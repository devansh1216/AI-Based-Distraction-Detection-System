# Classroom Distraction Detection System

## Project structure

- `backend/app/` contains the FastAPI application, API routes, database
  models, schemas, and services.
- `backend/alembic/` contains database migrations.
- `backend/requirements.txt` lists Python dependencies.
- `frontend/` contains the dashboard, browser camera detector, styles, and
  static assets served by FastAPI.
- `docs/` contains the project's requirements and design documents.

The local `.env`, Python environment, and SQLite database are runtime files,
not source files; keep them local and out of version control.

## Run locally

The FastAPI backend serves the frontend and uses SQLite by default. From the
repository root, run:

```powershell
Set-Location backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m app.scripts.create_admin
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open the application at <http://127.0.0.1:8000/>. API documentation is at
<http://127.0.0.1:8000/docs> and the health check is at
<http://127.0.0.1:8000/health>.

The local bootstrap account is `admin@example.com` / `Admin@123`.

The frontend supports administrator login and management of classrooms,
cameras, monitoring sessions, users, alerts, detection events, and reports.
During an active session, choose **Run local detector** to request camera
access and run MediaPipe face detection, face landmarks, and COCO object
detection in the browser. The object detector includes a `cell phone` class.
The first run downloads the models and browser runtime from their public CDNs,
so internet access is required. Use `http://localhost` or `http://127.0.0.1`
(secure contexts are required for browser camera access).

Face and object boxes are displayed locally; a sustained phone detection can
be recorded as a `PHONE_DETECTED` event. Head-turn and head-lower cues remain
experimental pose heuristics, not measures of attention or proof of
distraction. The detector does not identify people or infer peer
conversation. Video and face landmarks stay in the browser; only detection
metadata is sent to the local API. Camera access still depends on browser
permission and an available camera.

For PostgreSQL deployments, apply the new phone event enum values with
`alembic upgrade head` before starting the updated backend. SQLite local
development creates the current schema automatically.