const API_ROOT = "/api/v1";
const TOKEN_KEY = "classroomFocusToken";
const PHONE_EVENT_MIN_SCORE = 0.35;
const PHONE_CONFIRMATION_MS = 1400;
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
let cameraPreviewStream = null;
let detectorModulePromise = null;

const state = {
  token: sessionStorage.getItem(TOKEN_KEY),
  user: null,
  page: "overview",
  detection: null,
  data: {
    classrooms: [],
    cameras: [],
    sessions: [],
    alerts: [],
    events: [],
    reports: [],
    users: [],
  },
};

const pageDetails = {
  overview: ["Overview", "A live snapshot of classroom monitoring and activity."],
  classrooms: ["Classrooms", "Organize learning spaces and their capacity."],
  cameras: ["Cameras", "Register camera records and assign them to classrooms."],
  sessions: ["Monitoring sessions", "Run the local detector during an active session."],
  alerts: ["Alerts", "Review and acknowledge detected distraction alerts."],
  events: ["Detection events", "Review face, object, and head-pose detection events."],
  reports: ["Reports", "Review report records for completed monitoring sessions."],
  users: ["Users", "Manage administrator and teacher accounts."],
};

const alertLabels = {
  LOOKING_AWAY: "Looking away",
  HEAD_DOWN: "Head down",
  PHONE_DETECTED: "Mobile phone detected",
  PEER_CONVERSATION: "Peer conversation",
};

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  })[character]);
}

function formatDate(value, options = {}) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
    ...options,
  }).format(date);
}

function formatStatus(value) {
  return String(value || "UNKNOWN").replaceAll("_", " ").toLowerCase()
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function statusPill(value) {
  const status = String(value || "unknown").toLowerCase();
  return `<span class="status-pill status-${escapeHtml(status)}">${escapeHtml(formatStatus(value))}</span>`;
}

function setLoginMessage(message = "") {
  $("#login-error").textContent = message;
}

function showLogin() {
  $("#app-shell").classList.add("is-hidden");
  $("#login-screen").classList.remove("is-hidden");
}

function showApplication() {
  $("#login-screen").classList.add("is-hidden");
  $("#app-shell").classList.remove("is-hidden");
}

function clearSession() {
  state.token = null;
  state.user = null;
  sessionStorage.removeItem(TOKEN_KEY);
  const dialog = $("#app-dialog");
  if (dialog.open) dialog.close();
  stopCameraPreview();
  showLogin();
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set("Accept", "application/json");
  if (state.token) headers.set("Authorization", `Bearer ${state.token}`);
  if (options.body && !(options.body instanceof FormData)) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(`${API_ROOT}${path}`, { ...options, headers });
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await response.json() : null;

  if (response.status === 401 && state.token) {
    clearSession();
  }
  if (!response.ok) {
    const details = Array.isArray(body?.errors)
      ? body.errors.map((item) => `${(item.loc || []).slice(1).join(".")}: ${item.msg}`).join("; ")
      : Array.isArray(body?.detail)
        ? body.detail.map((item) => item.msg || JSON.stringify(item)).join("; ")
        : body?.detail || body?.message || `Request failed (${response.status})`;
    throw new Error(String(details));
  }
  return body;
}

function showToast(message, isError = false) {
  const toast = document.createElement("div");
  toast.className = `toast${isError ? " toast-error" : ""}`;
  toast.textContent = message;
  $("#toast-region").append(toast);
  window.setTimeout(() => toast.remove(), 3800);
}

function setPage(page) {
  if (!pageDetails[page]) return;
  state.page = page;
  $$(".nav-item[data-page]").forEach((item) => {
    item.classList.toggle("is-active", item.dataset.page === page);
  });
  $("#breadcrumb-current").textContent = pageDetails[page][0];
  renderPage();
}

function pageHeading(page, action = "") {
  const [title, description] = pageDetails[page];
  return `
    <div class="page-heading">
      <div><h1>${escapeHtml(title)}</h1><p>${escapeHtml(description)}</p></div>
      ${action ? `<div class="heading-actions">${action}</div>` : ""}
    </div>`;
}

function actionButton(label, action, id, style = "button-secondary") {
  return `<button class="button ${style} button-small" type="button" data-action="${escapeHtml(action)}" data-id="${escapeHtml(id)}">${escapeHtml(label)}</button>`;
}

function emptyState(title, message, action = "") {
  return `<div class="empty-state"><strong>${escapeHtml(title)}</strong>${escapeHtml(message)}${action}</div>`;
}

function renderMetric(label, value, icon, note) {
  return `<article class="metric-card">
    <div class="metric-top"><span>${escapeHtml(label)}</span><span class="metric-icon">${icon}</span></div>
    <div class="metric-value">${escapeHtml(value)}</div>
    <div class="metric-note">${escapeHtml(note)}</div>
  </article>`;
}

function renderOverview() {
  const { classrooms, cameras, sessions, alerts, events } = state.data;
  const activeSessions = sessions.filter((item) => item.session_status === "ACTIVE").length;
  const activeAlerts = alerts.filter((item) => item.status === "ACTIVE");
  const recentAlerts = [...alerts].sort((a, b) => new Date(b.generated_at) - new Date(a.generated_at)).slice(0, 5);
  const recentSessions = [...sessions].sort((a, b) => new Date(b.started_at) - new Date(a.started_at)).slice(0, 5);

  const activityContent = recentAlerts.length
    ? recentAlerts.map((alert) => `
      <div class="activity-row">
        <span class="activity-mark ${String(alert.severity).toLowerCase() === "high" ? "high" : ""}">!</span>
        <span class="activity-info">
          <strong>${escapeHtml(alertLabels[alert.alert_type] || formatStatus(alert.alert_type))} · ${escapeHtml(alert.tracking_id)}</strong>
          <small>${escapeHtml(formatDate(alert.generated_at))} · ${escapeHtml(formatStatus(alert.severity))} severity</small>
        </span>
        ${statusPill(alert.status)}
      </div>`).join("")
    : emptyState("All clear", "No alerts have been recorded yet.");

  const sessionContent = recentSessions.length
    ? recentSessions.map((session) => {
      const classroom = state.data.classrooms.find((item) => item.id === session.classroom_id);
      return `<div class="session-row">
        <span class="session-symbol">◷</span>
        <span><strong>${escapeHtml(classroom?.classroom_name || `Classroom ${session.classroom_id}`)}</strong><small>Started ${escapeHtml(formatDate(session.started_at))}</small></span>
        ${statusPill(session.session_status)}
      </div>`;
    }).join("")
    : emptyState("No sessions yet", "Create a session after registering a classroom and camera.",
      '<button class="button button-primary button-small" type="button" data-go="sessions">Start a session</button>');

  return `${pageHeading("overview")}
    <section class="metrics-grid" aria-label="Workspace summary">
      ${renderMetric("CLASSROOMS", classrooms.length, "▦", "Registered learning spaces")}
      ${renderMetric("ACTIVE SESSIONS", activeSessions, "◷", `${sessions.length} total sessions`)}
      ${renderMetric("ACTIVE ALERTS", activeAlerts.length, "!", `${alerts.length} total alerts`)}
      ${renderMetric("DETECTION CUES", events.length, "⌁", `${cameras.length} registered cameras`)}
    </section>
    <section class="overview-grid">
      <article class="panel">
        <header class="panel-header"><div><h2>Recent alerts</h2><p>Latest activity across monitored classrooms</p></div><button class="text-button" type="button" data-go="alerts">View all</button></header>
        <div class="activity-list">${activityContent}</div>
      </article>
      <article class="panel">
        <header class="panel-header"><div><h2>Monitoring sessions</h2><p>Recently created sessions</p></div><button class="text-button" type="button" data-go="sessions">View all</button></header>
        <div class="session-list">${sessionContent}</div>
      </article>
    </section>
    <aside class="notice"><span class="notice-icon">i</span><span>Run the local detector during a session to see face boxes and COCO object labels, including mobile phones. Head-pose and object scores are estimates, not proof of distraction; video and face images are not stored or uploaded.</span></aside>`;
}

function tableMarkup(headers, rows, emptyMessage) {
  if (!rows.length) {
    return `<div class="table-panel">${emptyState("Nothing here yet", emptyMessage)}</div>`;
  }
  return `<div class="table-panel"><div class="table-wrap"><table><thead><tr>${headers.map((header) => `<th>${escapeHtml(header)}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody></table></div></div>`;
}

function renderClassrooms() {
  const rows = state.data.classrooms.map((classroom) => {
    const cameras = state.data.cameras.filter((camera) => camera.classroom_id === classroom.id).length;
    return `<tr>
      <td><span class="cell-primary">${escapeHtml(classroom.classroom_name)}</span><span class="cell-secondary">${escapeHtml(classroom.classroom_code)}</span></td>
      <td>${escapeHtml(classroom.building_name || "—")}${classroom.floor_number === null ? "" : `<span class="cell-secondary">Floor ${escapeHtml(classroom.floor_number)}</span>`}</td>
      <td>${escapeHtml(classroom.max_capacity)}</td>
      <td>${cameras}</td>
      <td>${statusPill(classroom.is_active ? "ACTIVE" : "INACTIVE")}</td>
      <td><div class="table-actions">${actionButton(classroom.is_active ? "Deactivate" : "Activate", "toggle-classroom", classroom.id)}</div></td>
    </tr>`;
  });
  return `${pageHeading("classrooms", '<button class="button button-primary" type="button" data-action="add-classroom">+ Add classroom</button>')}
    ${tableMarkup(["CLASSROOM", "LOCATION", "CAPACITY", "CAMERAS", "STATUS", ""], rows, "Add your first classroom to begin setting up monitoring.")}`;
}

function renderCameras() {
  const rows = state.data.cameras.map((camera) => {
    const classroom = state.data.classrooms.find((item) => item.id === camera.classroom_id);
    return `<tr>
      <td><span class="cell-primary">${escapeHtml(camera.camera_name)}</span><span class="cell-secondary">ID ${escapeHtml(camera.id)}</span></td>
      <td>${escapeHtml(classroom?.classroom_name || `Classroom ${camera.classroom_id}`)}</td>
      <td><span class="cell-primary">${escapeHtml(camera.camera_type)}</span><span class="cell-secondary">${escapeHtml(camera.resolution || "Resolution not set")}</span></td>
      <td><span class="cell-primary">${escapeHtml(camera.camera_source)}</span><span class="cell-secondary">${camera.fps ? `${escapeHtml(camera.fps)} FPS` : "FPS not set"}</span></td>
      <td>${statusPill(camera.is_active ? "ACTIVE" : "INACTIVE")}</td>
      <td><div class="table-actions">${actionButton(camera.is_active ? "Deactivate" : "Activate", "toggle-camera", camera.id)}</div></td>
    </tr>`;
  });
  const action = `${state.data.classrooms.length
    ? '<button class="button button-primary" type="button" data-action="add-camera">+ Register camera</button>'
    : '<button class="button button-secondary" type="button" data-go="classrooms">Add a classroom first</button>'}
    <button class="button button-secondary" type="button" data-action="preview-laptop-camera">Preview laptop camera</button>`;
  return `${pageHeading("cameras", action)}
    <aside class="notice"><span class="notice-icon">i</span><span>Face and object models run locally in this browser. Start a monitoring session and choose “Run local detector” to request camera access. The detector uses the browser's default camera; video and face images are never saved or uploaded.</span></aside>
    ${tableMarkup(["CAMERA", "CLASSROOM", "TYPE", "SOURCE", "STATUS", ""], rows, "Register a camera and assign it to a classroom.")}`;
}

function renderSessions() {
  const activeClassroomIds = new Set(
    state.data.classrooms.filter((classroom) => classroom.is_active).map((classroom) => classroom.id),
  );
  const canStart = state.data.cameras.some((camera) => camera.is_active && activeClassroomIds.has(camera.classroom_id));
  const rows = [...state.data.sessions].sort((a, b) => new Date(b.started_at) - new Date(a.started_at)).map((session) => {
    const classroom = state.data.classrooms.find((item) => item.id === session.classroom_id);
    const camera = state.data.cameras.find((item) => item.id === session.camera_id);
    const user = state.data.users.find((item) => item.id === session.user_id);
    const isActive = session.session_status === "ACTIVE" || session.session_status === "FINALIZING";
    const isDetecting = state.detection?.sessionId === session.id;
    const action = isActive
      ? `${actionButton(isDetecting ? "Stop detector" : "Run local detector", isDetecting ? "stop-detector" : "start-detector", session.id, isDetecting ? "button-danger" : "button-primary")}${actionButton("Complete", "complete-session", session.id)}`
      : "";
    return `<tr>
      <td><span class="cell-primary">Session #${escapeHtml(session.id)}</span><span class="cell-secondary">${escapeHtml(formatDate(session.started_at))}</span></td>
      <td>${escapeHtml(classroom?.classroom_name || `Classroom ${session.classroom_id}`)}</td>
      <td>${escapeHtml(camera?.camera_name || `Camera ${session.camera_id}`)}</td>
      <td>${escapeHtml(user?.full_name || `User ${session.user_id}`)}</td>
      <td>${statusPill(session.session_status)}</td>
      <td>${escapeHtml(session.total_events)} events · ${escapeHtml(session.total_alerts)} alerts</td>
      <td><div class="table-actions">${action}</div></td>
    </tr>`;
  });
  const action = canStart
    ? '<button class="button button-primary" type="button" data-action="add-session">+ Start session</button>'
    : '<button class="button button-secondary" type="button" data-go="cameras">Set up classroom and camera first</button>';
  return `${pageHeading("sessions", action)}
    ${tableMarkup(["SESSION", "CLASSROOM", "CAMERA", "OWNER", "STATUS", "ACTIVITY", ""], rows, "No monitoring sessions have been created yet.")}
    <aside class="notice"><span class="notice-icon">i</span><span>Face boxes and COCO object labels, including mobile phones, are processed locally. Sustained phone detections and approximate head-pose cues may be recorded; this is not a measure of attention.</span></aside>`;
}

function renderAlerts() {
  const rows = [...state.data.alerts].sort((a, b) => new Date(b.generated_at) - new Date(a.generated_at)).map((alert) => {
    const session = state.data.sessions.find((item) => item.id === alert.session_id);
    const actions = alert.status === "ACTIVE"
      ? `${actionButton("Acknowledge", "ack-alert", alert.id)}${actionButton("Dismiss", "dismiss-alert", alert.id, "button-danger")}`
      : "";
    return `<tr>
      <td><span class="cell-primary">${escapeHtml(alertLabels[alert.alert_type] || formatStatus(alert.alert_type))}</span><span class="cell-secondary">Tracking ${escapeHtml(alert.tracking_id)}</span></td>
      <td>${escapeHtml(session ? `Session #${session.id}` : `Session ${alert.session_id}`)}</td>
      <td><span class="severity-label">${escapeHtml(formatStatus(alert.severity))}</span></td>
      <td>${statusPill(alert.status)}</td>
      <td>${escapeHtml(formatDate(alert.generated_at))}</td>
      <td><div class="table-actions">${actions}</div></td>
    </tr>`;
  });
  return `${pageHeading("alerts")}
    ${tableMarkup(["BEHAVIOR", "SESSION", "SEVERITY", "STATUS", "RECEIVED", ""], rows, "Alerts will appear here when the local detector records a sustained cue.")}`;
}

function renderEvents() {
  const rows = [...state.data.events].sort((a, b) => new Date(b.event_timestamp) - new Date(a.event_timestamp)).map((event) => {
    return `<tr>
      <td><span class="cell-primary">${escapeHtml(alertLabels[event.behaviour_type] || formatStatus(event.behaviour_type))}</span><span class="cell-secondary">Tracking ${escapeHtml(event.tracking_id)}</span></td>
      <td>Session #${escapeHtml(event.session_id)}</td>
      <td>${Math.round(Number(event.confidence_score) * 100)}% detection score</td>
      <td>${escapeHtml(formatDate(event.event_timestamp))}</td>
    </tr>`;
  });
  return `${pageHeading("events")}
    ${tableMarkup(["DETECTION", "SESSION", "SCORE", "DETECTED AT"], rows, "Start a local detector during an active session to record sustained phone or head-pose cues.")}`;
}

function renderReports() {
  const rows = [...state.data.reports].sort((a, b) => new Date(b.created_at) - new Date(a.created_at)).map((report) => `
    <tr>
      <td><span class="cell-primary">${escapeHtml(report.report_name)}</span><span class="cell-secondary">Report #${escapeHtml(report.id)}</span></td>
      <td>Session #${escapeHtml(report.session_id)}</td>
      <td>${statusPill(report.report_status)}</td>
      <td>${escapeHtml(formatDate(report.generated_at || report.created_at))}</td>
      <td><span class="cell-primary">${escapeHtml(report.report_path)}</span></td>
    </tr>`).join("");
  return `${pageHeading("reports")}
    ${tableMarkup(["REPORT", "SESSION", "STATUS", "DATE", "FILE LOCATION"], rows ? [rows] : [], "Reports will be listed here once generated by a report service.")}`;
}

function renderUsers() {
  const rows = state.data.users.map((user) => `
    <tr>
      <td><span class="cell-primary">${escapeHtml(user.full_name)}</span><span class="cell-secondary">User #${escapeHtml(user.id)}</span></td>
      <td>${escapeHtml(user.email)}</td>
      <td>${escapeHtml(formatStatus(user.role))}</td>
      <td>${statusPill(user.is_active ? "ACTIVE" : "INACTIVE")}</td>
      <td>${escapeHtml(user.last_login_at ? formatDate(user.last_login_at) : "Never")}</td>
      <td><div class="table-actions">${user.id === state.user.id ? '<span class="cell-secondary">You</span>' : actionButton(user.is_active ? "Deactivate" : "Activate", "toggle-user", user.id)}</div></td>
    </tr>`);
  return `${pageHeading("users", '<button class="button button-primary" type="button" data-action="add-user">+ Add user</button>')}
    ${tableMarkup(["USER", "EMAIL", "ROLE", "STATUS", "LAST LOGIN", ""], rows, "No user accounts were found.")}`;
}

function renderPage() {
  const content = $("#page-content");
  if (!content) return;
  const renderers = {
    overview: renderOverview,
    classrooms: renderClassrooms,
    cameras: renderCameras,
    sessions: renderSessions,
    alerts: renderAlerts,
    events: renderEvents,
    reports: renderReports,
    users: renderUsers,
  };
  content.innerHTML = renderers[state.page]();
  $("#alert-count").textContent = state.data.alerts.filter((alert) => alert.status === "ACTIVE").length;
}

async function loadData() {
  $("#page-content").innerHTML = '<div class="loading">Loading workspace data…</div>';
  try {
    const [classrooms, cameras, sessions, alerts, events, reports, userResponse] = await Promise.all([
      request("/classrooms"),
      request("/cameras"),
      request("/monitoring-sessions"),
      request("/alerts"),
      request("/detection-events"),
      request("/reports"),
      request("/users"),
    ]);
    state.data = {
      classrooms,
      cameras,
      sessions,
      alerts,
      events,
      reports,
      users: userResponse.users || [],
    };
    renderPage();
  } catch (error) {
    if (state.token) {
      $("#page-content").innerHTML = `<div class="table-panel">${emptyState("Could not load workspace", error.message, '<button class="button button-secondary button-small" type="button" id="retry-button">Try again</button>')}</div>`;
      $("#retry-button")?.addEventListener("click", loadData);
    }
  }
}

function setUserDetails(user) {
  $("#user-name").textContent = user.full_name;
  $("#user-role").textContent = formatStatus(user.role);
  $("#user-avatar").textContent = (user.full_name || "A").trim().charAt(0).toUpperCase();
}

async function bootstrap() {
  if (!state.token) {
    showLogin();
    return;
  }
  try {
    state.user = await request("/auth/me");
    if (state.user.role !== "ADMINISTRATOR") {
      clearSession();
      setLoginMessage("This workspace is currently available to administrators only.");
      return;
    }
    setUserDetails(state.user);
    showApplication();
    await loadData();
  } catch (error) {
    if (state.token) {
      clearSession();
      setLoginMessage(error.message || "Please sign in again.");
    }
  }
}

function field(name, label, type = "text", options = {}) {
  const id = options.id || name;
  const required = options.required === false ? "" : "required";
  const hint = options.hint ? `<small class="field-hint">${escapeHtml(options.hint)}</small>` : "";
  const attributes = [
    options.min !== undefined ? `min="${escapeHtml(options.min)}"` : "",
    options.max !== undefined ? `max="${escapeHtml(options.max)}"` : "",
    options.maxlength ? `maxlength="${escapeHtml(options.maxlength)}"` : "",
    options.placeholder ? `placeholder="${escapeHtml(options.placeholder)}"` : "",
    options.autocomplete ? `autocomplete="${escapeHtml(options.autocomplete)}"` : "",
  ].filter(Boolean).join(" ");

  if (options.choices) {
    return `<div class="form-field"><label for="${escapeHtml(id)}">${escapeHtml(label)}</label><select id="${escapeHtml(id)}" name="${escapeHtml(name)}" ${required}>${options.choices}</select>${hint}</div>`;
  }
  return `<div class="form-field"><label for="${escapeHtml(id)}">${escapeHtml(label)}</label><input id="${escapeHtml(id)}" name="${escapeHtml(name)}" type="${escapeHtml(type)}" ${required} ${attributes}>${hint}</div>`;
}

function openDialog({ title, description, fields, onSubmit, setup }) {
  const dialog = $("#app-dialog");
  $("#dialog-content").innerHTML = `
    <header class="dialog-header"><div><h2>${escapeHtml(title)}</h2><p>${escapeHtml(description)}</p></div><button class="dialog-close" type="button" aria-label="Close dialog">×</button></header>
    <form id="entity-form" class="dialog-form">${fields}<p id="dialog-error" class="dialog-error" role="alert"></p>
      <div class="dialog-actions"><button class="button button-secondary" type="button" data-close-dialog>Cancel</button><button class="button button-primary" type="submit">Save</button></div>
    </form>`;
  dialog.showModal();
  $$(".dialog-close, [data-close-dialog]", dialog).forEach((button) => button.addEventListener("click", () => dialog.close()));
  setup?.();
  $("#entity-form", dialog).addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const submit = $('button[type="submit"]', form);
    const errorNode = $("#dialog-error", form);
    submit.disabled = true;
    errorNode.textContent = "";
    try {
      await onSubmit(new FormData(form), form);
      dialog.close();
      showToast("Changes saved.");
      await loadData();
    } catch (error) {
      errorNode.textContent = error.message;
      submit.disabled = false;
    }
  });
}

function stopCameraPreview() {
  if (state.detection) stopDetection(state.detection);
  if (cameraPreviewStream) {
    cameraPreviewStream.getTracks().forEach((track) => track.stop());
    cameraPreviewStream = null;
  }
  const video = $("#camera-preview-video");
  if (video) video.srcObject = null;
}

function stopDetection(run) {
  run.active = false;
  if (run.timer) window.clearTimeout(run.timer);
  if (run.stream) {
    run.stream.getTracks().forEach((track) => track.stop());
    run.stream = null;
  }
  for (const task of [run.faceDetector, run.objectDetector, run.faceLandmarker]) {
    task?.close();
  }
  run.faceDetector = null;
  run.objectDetector = null;
  run.faceLandmarker = null;
  if (state.detection === run) state.detection = null;
}

function detectorStatus(message) {
  const status = $("#detector-status");
  if (status) status.textContent = message;
}

function loadDetectorModule() {
  if (!detectorModulePromise) {
    detectorModulePromise = import("/detector.js").catch((error) => {
      detectorModulePromise = null;
      throw error;
    });
  }
  return detectorModulePromise;
}

async function saveDetectedCue(run, behaviourType, confidence) {
  const timestamp = new Date().toISOString();
  const event = {
    session_id: run.sessionId,
    tracking_id: "LOCAL-DEMO-1",
    behaviour_type: behaviourType,
    confidence_score: Math.max(0, Math.min(1, confidence)).toFixed(3),
    event_timestamp: timestamp,
  };

  try {
    await request("/detection-events", { method: "POST", body: JSON.stringify(event) });
  } catch (error) {
    detectorStatus(`Could not save detection cue: ${error.message}`);
    return;
  }

  run.savedCues += 1;
  const count = $("#detector-cue-count");
  if (count) count.textContent = String(run.savedCues);
  detectorStatus(`${alertLabels[behaviourType]} cue saved. Video stayed on this device.`);

  try {
    await request("/alerts", {
      method: "POST",
      body: JSON.stringify({
        session_id: run.sessionId,
        tracking_id: event.tracking_id,
        alert_type: behaviourType,
        severity: "LOW",
        status: "ACTIVE",
        generated_at: timestamp,
        acknowledged_at: null,
      }),
    });
    run.savedAlerts += 1;
    const alertCount = $("#detector-alert-count");
    if (alertCount) alertCount.textContent = String(run.savedAlerts);
  } catch (error) {
    detectorStatus(`Cue saved, but alert creation failed: ${error.message}`);
  }
}

function getDetectionCategory(detection) {
  const category = detection.categories?.[0];
  if (!category) return null;
  return {
    name: category.categoryName || category.displayName || "Object",
    score: Number(category.score) || 0,
  };
}

function drawDetectionOverlay(run, video) {
  const canvas = $("#detector-overlay");
  if (!canvas || !video.videoWidth || !video.videoHeight) return;
  if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
  }

  const context = canvas.getContext("2d");
  context.clearRect(0, 0, canvas.width, canvas.height);
  context.lineWidth = Math.max(3, canvas.width / 400);
  context.font = `${Math.max(18, canvas.width / 48)}px Segoe UI, sans-serif`;

  const drawBox = (box, label, color) => {
    if (!box) return;
    context.strokeStyle = color;
    context.fillStyle = color;
    context.strokeRect(box.originX, box.originY, box.width, box.height);
    const textY = Math.max(context.measureText(label).actualBoundingBoxAscent + 8, box.originY);
    context.fillRect(box.originX, textY - 24, context.measureText(label).width + 12, 26);
    context.fillStyle = "#fff";
    context.fillText(label, box.originX + 6, textY - 6);
  };

  for (const face of run.lastFaces) {
    const score = Math.round((face.categories?.[0]?.score || 0) * 100);
    drawBox(face.boundingBox, `Face ${score}%`, "#15966b");
  }

  for (const detection of run.lastObjects) {
    const category = getDetectionCategory(detection);
    if (!category) continue;
    const minScore = run.detectorModule.isPhoneCategory(category.name) ? 0.25 : 0.5;
    if (category.score < minScore) continue;
    const label = `${category.name} ${Math.round(category.score * 100)}%`;
    const color = run.detectorModule.isPhoneCategory(category.name) ? "#d05252" : "#4778e8";
    drawBox(detection.boundingBox, label, color);
  }
}

function updateDetectionSummary(run) {
  const faceResult = $("#detector-face-result");
  if (faceResult) {
    if (run.lastFaces.length) {
      const score = Math.round((run.lastFaces[0].categories?.[0]?.score || 0) * 100);
      faceResult.textContent = `Face detected · ${score}%`;
    } else {
      faceResult.textContent = "No face detected";
    }
  }

  const objectResult = $("#detector-object-result");
  if (objectResult) {
    const objects = run.lastObjects
      .map(getDetectionCategory)
      .filter((category) => category && category.score >= (run.detectorModule.isPhoneCategory(category.name) ? 0.25 : 0.5))
      .slice(0, 5)
      .map((category) => `${category.name} ${Math.round(category.score * 100)}%`);
    objectResult.textContent = objects.length ? `Objects: ${objects.join(", ")}` : "No objects detected above the display threshold";
  }
}

function trackPhoneCue(run, detections, now) {
  const phone = detections
    .map(getDetectionCategory)
    .filter((category) => category && run.detectorModule.isPhoneCategory(category.name) && category.score >= PHONE_EVENT_MIN_SCORE)
    .sort((left, right) => right.score - left.score)[0];
  const tracking = run.cues.PHONE_DETECTED;

  if (!phone) {
    if (tracking.lastSeenAt && now - tracking.lastSeenAt > 1500) {
      tracking.since = 0;
      tracking.hits = 0;
      tracking.sent = false;
    }
    return;
  }

  if (!tracking.since || now - tracking.lastSeenAt > 1500) {
    tracking.since = now;
    tracking.hits = 0;
  }
  tracking.lastSeenAt = now;
  tracking.hits += 1;
  if (tracking.sent || tracking.hits < 2 || now < tracking.cooldownUntil || now - tracking.since < PHONE_CONFIRMATION_MS || run.savingCue) return;

  tracking.sent = true;
  tracking.cooldownUntil = now + 30000;
  run.savingCue = true;
  detectorStatus(`Mobile phone detected (${Math.round(phone.score * 100)}%). Saving event metadata…`);
  saveDetectedCue(run, "PHONE_DETECTED", phone.score)
    .catch((error) => detectorStatus(`Phone detection event failed: ${error.message}`))
    .finally(() => { run.savingCue = false; });
}

function processDetectorFrame(run) {
  if (!run.active || !run.faceDetector || !run.objectDetector || !run.faceLandmarker) return;
  const video = $("#detector-video");

  if (video?.readyState >= HTMLMediaElement.HAVE_CURRENT_DATA && video.currentTime !== run.lastVideoTime) {
    try {
      const now = performance.now();
      run.lastVideoTime = video.currentTime;
      if (now - run.lastFaceDetectionAt >= 300) {
        run.lastFaces = run.faceDetector.detectForVideo(video, now).detections || [];
        run.lastFaceDetectionAt = now;
        if (!run.lastFaces.length) {
          run.baseline = null;
          run.samples = [];
          run.calibrationStartedAt = now;
          run.cues.LOOKING_AWAY.since = 0;
          run.cues.HEAD_DOWN.since = 0;
        }
      }

      if (now - run.lastObjectDetectionAt >= 700) {
        run.lastObjects = run.objectDetector.detectForVideo(video, now).detections || [];
        run.lastObjectDetectionAt = now;
        trackPhoneCue(run, run.lastObjects, now);
      }

      updateDetectionSummary(run);
      drawDetectionOverlay(run, video);

      if (run.lastFaces.length && now - run.lastPoseAt >= 500) {
        run.lastPoseAt = now;
        const landmarks = run.faceLandmarker.detectForVideo(video, now).faceLandmarks?.[0];
        const pose = landmarks && run.detectorModule.measureHeadPose(landmarks);
        if (!pose) {
          if (!run.baseline) detectorStatus("Face detected. Center your full face for head-pose calibration.");
        } else if (!run.baseline) {
          run.samples.push(pose);
          if (now - run.calibrationStartedAt < 2500 || run.samples.length < 4) {
            detectorStatus("Face detected. Look toward the camera to calibrate head pose.");
          } else {
            run.baseline = {
              yawOffset: run.detectorModule.median(run.samples.map((sample) => sample.yawOffset)),
              pitchRatio: run.detectorModule.median(run.samples.map((sample) => sample.pitchRatio)),
            };
            detectorStatus("Face and object detection active. Head-pose cues are approximate.");
          }
        } else {
          const yawChange = Math.abs(pose.yawOffset - run.baseline.yawOffset);
          const pitchChange = pose.pitchRatio - run.baseline.pitchRatio;
          const cues = [
            { type: "LOOKING_AWAY", amount: yawChange, threshold: 0.18 },
            { type: "HEAD_DOWN", amount: pitchChange, threshold: 0.09 },
          ];
          for (const cue of cues) {
            const tracking = run.cues[cue.type];
            if (cue.amount >= cue.threshold) {
              if (!tracking.since) tracking.since = now;
              if (!tracking.sent && now >= tracking.cooldownUntil && now - tracking.since >= 1800 && !run.savingCue) {
                tracking.sent = true;
                tracking.cooldownUntil = now + 30000;
                run.savingCue = true;
                const heuristicScore = Math.min(0.95, 0.5 + (cue.amount - cue.threshold) * 1.2);
                detectorStatus(`Possible ${alertLabels[cue.type].toLowerCase()} cue. Saving event metadata…`);
                saveDetectedCue(run, cue.type, heuristicScore)
                  .catch((error) => detectorStatus(`Detection event failed: ${error.message}`))
                  .finally(() => { run.savingCue = false; });
              }
            } else {
              tracking.since = 0;
              tracking.sent = false;
            }
          }
          if (!run.savingCue) detectorStatus("Face and object detection active. Head-pose cues are approximate.");
        }
      } else if (!run.lastFaces.length && !run.savingCue) {
        detectorStatus("No face detected. Adjust lighting and keep your face inside the frame.");
      }
    } catch (error) {
      stopDetection(run);
      detectorStatus(`Detector stopped after an error: ${error.message}`);
    }
  }

  if (run.active) run.timer = window.setTimeout(() => processDetectorFrame(run), 250);
}

function startDetector(sessionId) {
  if (state.detection) return showToast("Stop the current local detector before starting another.", true);
  if (!navigator.mediaDevices?.getUserMedia) {
    return showToast("This browser does not support camera access on this page.", true);
  }

  let cameraRequest;
  try {
    cameraRequest = navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 1280 }, height: { ideal: 720 }, frameRate: { ideal: 15, max: 20 } },
      audio: false,
    });
  } catch (error) {
    return showToast(`Could not request the camera: ${error.message}`, true);
  }

  const dialog = $("#app-dialog");
  const run = {
    sessionId: Number(sessionId),
    active: true,
    stream: null,
    faceDetector: null,
    objectDetector: null,
    faceLandmarker: null,
    detectorModule: null,
    timer: null,
    lastVideoTime: -1,
    lastFaceDetectionAt: 0,
    lastObjectDetectionAt: 0,
    lastPoseAt: 0,
    lastFaces: [],
    lastObjects: [],
    calibrationStartedAt: 0,
    samples: [],
    baseline: null,
    savingCue: false,
    savedCues: 0,
    savedAlerts: 0,
    cues: {
      LOOKING_AWAY: { since: 0, sent: false, cooldownUntil: 0 },
      HEAD_DOWN: { since: 0, sent: false, cooldownUntil: 0 },
      PHONE_DETECTED: { since: 0, sent: false, cooldownUntil: 0, hits: 0, lastSeenAt: 0 },
    },
  };
  state.detection = run;
  $("#dialog-content").innerHTML = `
    <header class="dialog-header">
      <div><h2>Local face and object detection</h2><p>Session #${escapeHtml(sessionId)} · no identity recognition</p></div>
      <button class="dialog-close" type="button" aria-label="Close detector">×</button>
    </header>
    <div class="camera-preview">
      <div class="detector-video-wrap">
        <video id="detector-video" autoplay playsinline muted></video>
        <canvas id="detector-overlay" aria-hidden="true"></canvas>
      </div>
      <p id="detector-status" class="camera-preview-status" role="status">Requesting camera permission…</p>
      <div class="detector-results" aria-live="polite">
        <span id="detector-face-result">Waiting for face scan…</span>
        <span id="detector-object-result">Waiting for object scan…</span>
      </div>
      <div class="detector-counters">
        <span><strong id="detector-cue-count">0</strong><small>Saved cues</small></span>
        <span><strong id="detector-alert-count">0</strong><small>Alerts</small></span>
      </div>
      <aside class="notice"><span class="notice-icon">i</span><span>Face boxes and objects are detected locally. Video and face images stay on this device. Phone events require repeated 35%+ detections; only sustained phone and approximate head-pose cue metadata is sent to the server.</span></aside>
      <div class="dialog-actions"><button class="button button-danger" type="button" data-stop-detector>Stop camera and detector</button></div>
    </div>`;
  dialog.addEventListener("close", () => {
    stopDetection(run);
    renderPage();
    if (state.token) loadData();
  }, { once: true });
  $$(".dialog-close, [data-stop-detector]", dialog).forEach((button) => {
    button.addEventListener("click", () => dialog.close());
  });
  dialog.showModal();
  renderPage();

  cameraRequest.then(async (stream) => {
    if (!run.active) {
      stream.getTracks().forEach((track) => track.stop());
      return;
    }
    run.stream = stream;
    const video = $("#detector-video");
    if (!video) {
      stopDetection(run);
      return;
    }
    video.srcObject = stream;
    await video.play();
    detectorStatus("Loading face, phone, and landmark models. The first load may take a little while.");
    run.detectorModule = await loadDetectorModule();
    const detectors = await run.detectorModule.createLocalDetectors(detectorStatus);
    run.faceDetector = detectors.faceDetector;
    run.objectDetector = detectors.objectDetector;
    run.faceLandmarker = detectors.faceLandmarker;
    if (!run.active) {
      stopDetection(run);
      return;
    }
    run.calibrationStartedAt = performance.now();
    detectorStatus("Models ready. Face and object scans are starting.");
    processDetectorFrame(run);
  }).catch((error) => {
    if (!run.active) return;
    const reason = error.name === "NotAllowedError"
      ? "Camera permission denied. Allow access in the browser's site settings, then try again."
      : error.name === "NotFoundError"
        ? "No camera was found. Check that the built-in laptop camera is enabled."
        : error.name === "NotReadableError"
          ? "The camera is busy in another app. Close that app and try again."
          : `Could not start the local detector: ${error.message || error.name}.`;
    stopDetection(run);
    detectorStatus(reason);
  });
}

function openCameraPreview() {
  if (!navigator.mediaDevices?.getUserMedia) {
    return showToast("This browser does not support camera access on this page.", true);
  }

  const dialog = $("#app-dialog");
  $("#dialog-content").innerHTML = `
    <header class="dialog-header">
      <div><h2>Laptop camera preview</h2><p>Allow camera access in your browser when prompted. No video is saved or sent to the server.</p></div>
      <button class="dialog-close" type="button" aria-label="Close preview">×</button>
    </header>
    <div class="camera-preview">
      <video id="camera-preview-video" autoplay playsinline muted></video>
      <p id="camera-preview-status" class="camera-preview-status" role="status">Requesting camera permission…</p>
      <div class="dialog-actions"><button class="button button-secondary" type="button" data-stop-camera>Stop camera</button></div>
    </div>`;
  const streamRequest = navigator.mediaDevices.getUserMedia({
    video: { width: { ideal: 1280 }, height: { ideal: 720 } },
    audio: false,
  });
  dialog.showModal();
  dialog.addEventListener("close", stopCameraPreview, { once: true });
  $$(".dialog-close, [data-stop-camera]", dialog).forEach((button) => {
    button.addEventListener("click", () => dialog.close());
  });

  streamRequest.then((stream) => {
    if (!dialog.open) {
      stream.getTracks().forEach((track) => track.stop());
      return;
    }
    cameraPreviewStream = stream;
    $("#camera-preview-video").srcObject = stream;
    $("#camera-preview-status").textContent = "Camera is on. Video stays on this device.";
  }).catch((error) => {
    const status = $("#camera-preview-status");
    if (status && dialog.open) {
      const reason = error.name === "NotAllowedError"
        ? "Camera permission was denied. Allow camera access in the browser's site settings and try again."
        : error.name === "NotFoundError"
          ? "No camera was found on this device."
          : `Could not start the camera: ${error.message || error.name}.`;
      status.textContent = reason;
    }
  });
}

function addClassroom() {
  openDialog({
    title: "Add classroom",
    description: "Add a learning space to your workspace.",
    fields: [
      field("classroom_code", "Classroom code", "text", { placeholder: "e.g. CSE-101", maxlength: 20 }),
      field("classroom_name", "Classroom name", "text", { placeholder: "e.g. Computer Science Lab", maxlength: 100 }),
      field("building_name", "Building", "text", { required: false, placeholder: "e.g. Engineering Block", maxlength: 100 }),
      field("floor_number", "Floor", "number", { required: false, min: 0, max: 100, placeholder: "0" }),
      field("max_capacity", "Maximum capacity", "number", { min: 1, max: 500, placeholder: "60" }),
    ].join(""),
    onSubmit: async (form) => {
      const body = {
        classroom_code: form.get("classroom_code").trim(),
        classroom_name: form.get("classroom_name").trim(),
        building_name: form.get("building_name").trim() || null,
        floor_number: form.get("floor_number") === "" ? null : Number(form.get("floor_number")),
        max_capacity: Number(form.get("max_capacity")),
      };
      await request("/classrooms", { method: "POST", body: JSON.stringify(body) });
    },
  });
}

function addCamera() {
  if (!state.data.classrooms.length) return showToast("Create a classroom before registering a camera.", true);
  const choices = state.data.classrooms.map((classroom) => `<option value="${escapeHtml(classroom.id)}">${escapeHtml(classroom.classroom_code)} · ${escapeHtml(classroom.classroom_name)}</option>`).join("");
  openDialog({
    title: "Register camera",
    description: "Add a camera record for this classroom. The local demo uses the browser's default webcam.",
    fields: [
      field("classroom_id", "Classroom", "select", { choices }),
      field("camera_name", "Camera name", "text", { placeholder: "e.g. Front camera", maxlength: 100 }),
      field("camera_source", "Camera source", "text", { placeholder: "e.g. laptop webcam (browser default)", maxlength: 255, hint: "For the local demo this is descriptive only; the browser opens its default webcam. RTSP sources are not read by this demo." }),
      field("camera_type", "Camera type", "text", { placeholder: "WEBCAM, USB, IP…", maxlength: 30 }),
      field("resolution", "Resolution", "text", { required: false, placeholder: "1920x1080", maxlength: 20 }),
      field("fps", "Frames per second", "number", { required: false, min: 1, max: 240, placeholder: "30" }),
    ].join(""),
    onSubmit: async (form) => {
      const body = {
        classroom_id: Number(form.get("classroom_id")),
        camera_name: form.get("camera_name").trim(),
        camera_source: form.get("camera_source").trim(),
        camera_type: form.get("camera_type").trim(),
        resolution: form.get("resolution").trim() || null,
        fps: form.get("fps") === "" ? null : Number(form.get("fps")),
      };
      await request("/cameras", { method: "POST", body: JSON.stringify(body) });
    },
  });
}

function addSession() {
  const classrooms = state.data.classrooms.filter((classroom) => classroom.is_active);
  const activeClassroomIds = new Set(classrooms.map((classroom) => classroom.id));
  const availableCameras = state.data.cameras.filter(
    (camera) => camera.is_active && activeClassroomIds.has(camera.classroom_id),
  );
  if (!classrooms.length || !availableCameras.length) {
    return showToast("Add an active classroom and camera before starting a session.", true);
  }
  const classChoices = classrooms.map((classroom) => `<option value="${escapeHtml(classroom.id)}">${escapeHtml(classroom.classroom_name)}</option>`).join("");
  const cameraChoices = availableCameras.map((camera) => {
    const classroom = state.data.classrooms.find((item) => item.id === camera.classroom_id);
    return `<option value="${escapeHtml(camera.id)}" data-classroom-id="${escapeHtml(camera.classroom_id)}">${escapeHtml(camera.camera_name)} · ${escapeHtml(classroom?.classroom_name || "Classroom")}</option>`;
  }).join("");
  openDialog({
    title: "Start monitoring session",
    description: "Create a session record for an administrator and camera.",
    fields: [
      field("classroom_id", "Classroom", "select", { id: "session-classroom", choices: classChoices }),
      field("camera_id", "Camera", "select", { id: "session-camera", choices: cameraChoices }),
    ].join(""),
    setup: () => {
      const classSelect = $("#session-classroom");
      const cameraSelect = $("#session-camera");
      const filterCameras = () => {
        const classroomId = classSelect.value;
        const visible = [...cameraSelect.options].filter((option) => option.dataset.classroomId === classroomId);
        [...cameraSelect.options].forEach((option) => { option.hidden = option.dataset.classroomId !== classroomId; });
        if (visible.length) cameraSelect.value = visible[0].value;
      };
      classSelect.addEventListener("change", filterCameras);
      filterCameras();
    },
    onSubmit: async (form) => {
      await request("/monitoring-sessions", {
        method: "POST",
        body: JSON.stringify({
          user_id: state.user.id,
          classroom_id: Number(form.get("classroom_id")),
          camera_id: Number(form.get("camera_id")),
        }),
      });
    },
  });
}

function addUser() {
  openDialog({
    title: "Add user",
    description: "Create an administrator or teacher account.",
    fields: [
      field("full_name", "Full name", "text", { placeholder: "e.g. Alex Morgan", maxlength: 100 }),
      field("email", "Email address", "email", { placeholder: "alex@example.com", autocomplete: "email" }),
      field("password", "Temporary password", "password", { min: 8, maxlength: 128, autocomplete: "new-password", hint: "Use at least 8 characters." }),
      field("role", "Role", "select", { choices: '<option value="TEACHER">Teacher</option><option value="ADMINISTRATOR">Administrator</option>' }),
    ].join(""),
    onSubmit: async (form) => {
      await request("/users", {
        method: "POST",
        body: JSON.stringify({
          full_name: form.get("full_name").trim(),
          email: form.get("email").trim(),
          password: form.get("password"),
          role: form.get("role"),
          is_active: true,
        }),
      });
    },
  });
}

async function performAction(button) {
  const { action, id } = button.dataset;
  if (action === "add-classroom") return addClassroom();
  if (action === "add-camera") return addCamera();
  if (action === "preview-laptop-camera") return openCameraPreview();
  if (action === "start-detector") return startDetector(id);
  if (action === "stop-detector") {
    if (state.detection?.sessionId === Number(id)) $("#app-dialog").close();
    return;
  }
  if (action === "add-session") return addSession();
  if (action === "add-user") return addUser();
  if (action === "toggle-classroom" || action === "toggle-camera" || action === "toggle-user") {
    const resource = action.replace("toggle-", "");
    const item = state.data[resource === "classroom" ? "classrooms" : resource === "camera" ? "cameras" : "users"].find((row) => row.id === Number(id));
    if (!item) return;
    const endpoint = resource === "classroom" ? "classrooms" : resource === "camera" ? "cameras" : "users";
    const verb = item.is_active ? "deactivate" : "activate";
    await request(`/${endpoint}/${id}/${verb}`, { method: "PATCH" });
    showToast(`${resource[0].toUpperCase()}${resource.slice(1)} ${item.is_active ? "deactivated" : "activated"}.`);
    return loadData();
  }
  if (action === "complete-session") {
    await request(`/monitoring-sessions/${id}/complete`, { method: "PATCH" });
    showToast("Monitoring session completed.");
    return loadData();
  }
  if (action === "ack-alert" || action === "dismiss-alert") {
    const verb = action === "ack-alert" ? "acknowledge" : "dismiss";
    await request(`/alerts/${id}/${verb}`, { method: "PATCH" });
    showToast(`Alert ${action === "ack-alert" ? "acknowledged" : "dismissed"}.`);
    return loadData();
  }
}

$("#login-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const submit = $('button[type="submit"]', form);
  submit.disabled = true;
  setLoginMessage("");
  try {
    const body = new URLSearchParams({
      username: form.elements.username.value.trim(),
      password: form.elements.password.value,
    });
    const result = await fetch(`${API_ROOT}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded", Accept: "application/json" },
      body,
    });
    const payload = await result.json();
    if (!result.ok) throw new Error(payload.detail || payload.message || "Could not sign in.");
    state.token = payload.access_token;
    sessionStorage.setItem(TOKEN_KEY, state.token);
    await bootstrap();
  } catch (error) {
    setLoginMessage(error.message || "Could not connect to the backend.");
  } finally {
    submit.disabled = false;
  }
});

$$(".nav-item[data-page]").forEach((button) => button.addEventListener("click", () => setPage(button.dataset.page)));
$("#logout-button").addEventListener("click", clearSession);
$("#refresh-button").addEventListener("click", loadData);
$("#page-content").addEventListener("click", async (event) => {
  const go = event.target.closest("[data-go]");
  if (go) return setPage(go.dataset.go);
  const button = event.target.closest("[data-action]");
  if (!button) return;
  button.disabled = true;
  try {
    await performAction(button);
  } catch (error) {
    showToast(error.message, true);
  } finally {
    if (button.isConnected) button.disabled = false;
  }
});
$("#today-label").textContent = new Intl.DateTimeFormat(undefined, { weekday: "short", month: "short", day: "numeric" }).format(new Date());
window.addEventListener("pagehide", stopCameraPreview);

bootstrap();
