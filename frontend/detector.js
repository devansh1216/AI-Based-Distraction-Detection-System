const MEDIAPIPE_VERSION = "1.2.3";
const MEDIAPIPE_BASE = `https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@${MEDIAPIPE_VERSION}`;
const FACE_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite";
const LANDMARK_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task";
const OBJECT_MODEL_URL = "https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite2/float32/1/efficientdet_lite2.tflite";

let runtimePromise;

async function loadRuntime() {
  if (!runtimePromise) {
    runtimePromise = (async () => {
      const vision = await import(`${MEDIAPIPE_BASE}/vision_bundle.mjs`);
      const fileset = await vision.FilesetResolver.forVisionTasks(`${MEDIAPIPE_BASE}/wasm`);
      return { vision, fileset };
    })().catch((error) => {
      runtimePromise = null;
      throw error;
    });
  }
  return runtimePromise;
}

export async function createLocalDetectors(onStatus) {
  const { vision, fileset } = await loadRuntime();
  let faceDetector;
  let objectDetector;
  let faceLandmarker;

  try {
    onStatus("Loading face detector…");
    faceDetector = await vision.FaceDetector.createFromOptions(fileset, {
      baseOptions: { modelAssetPath: FACE_MODEL_URL, delegate: "CPU" },
      runningMode: "VIDEO",
      minDetectionConfidence: 0.3,
      minSuppressionThreshold: 0.3,
    });

    onStatus("Loading phone and object detector. The first download may take a little while…");
    objectDetector = await vision.ObjectDetector.createFromOptions(fileset, {
      baseOptions: { modelAssetPath: OBJECT_MODEL_URL, delegate: "CPU" },
      runningMode: "VIDEO",
      scoreThreshold: 0.1,
      maxResults: 20,
    });

    onStatus("Loading facial landmarks for head-pose cues…");
    faceLandmarker = await vision.FaceLandmarker.createFromOptions(fileset, {
      baseOptions: { modelAssetPath: LANDMARK_MODEL_URL, delegate: "CPU" },
      runningMode: "VIDEO",
      numFaces: 1,
      minFaceDetectionConfidence: 0.35,
      minFacePresenceConfidence: 0.35,
      minTrackingConfidence: 0.45,
    });

    return { faceDetector, objectDetector, faceLandmarker };
  } catch (error) {
    faceDetector?.close();
    objectDetector?.close();
    faceLandmarker?.close();
    throw new Error(`Local detection models could not start: ${error.message || error}`);
  }
}

export function measureHeadPose(landmarks) {
  const leftEye = landmarks[33];
  const rightEye = landmarks[263];
  const nose = landmarks[1];
  const chin = landmarks[152];
  if (!leftEye || !rightEye || !nose || !chin) return null;

  const eyeCenterX = (leftEye.x + rightEye.x) / 2;
  const eyeLineY = (leftEye.y + rightEye.y) / 2;
  const eyeSpan = Math.abs(rightEye.x - leftEye.x);
  const faceHeight = chin.y - eyeLineY;
  if (eyeSpan < 0.001 || faceHeight < 0.02) return null;

  return {
    yawOffset: (nose.x - eyeCenterX) / eyeSpan,
    pitchRatio: (nose.y - eyeLineY) / faceHeight,
  };
}

export function isPhoneCategory(name) {
  return /^(cell|mobile)\s*phone$|^smartphone$|^phone$/i.test(String(name || "").trim());
}

export function median(values) {
  if (!values.length) return 0;
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}
