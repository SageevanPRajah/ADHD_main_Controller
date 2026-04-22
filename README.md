# ADHD Main Backend Gateway

A FastAPI gateway that sits between the React frontend and the two ADHD microservices.

## Architecture

Frontend (`http://localhost:5173`)
→ Gateway (`http://localhost:8000`)
→ Body Posture Backend (`http://localhost:8001`)
→ Eye Tracking Backend (`http://localhost:8004`)

## What this gateway does

- Accepts frontend requests on port `8000`
- Proxies body posture video uploads to the posture backend
- Proxies eye-tracking JSON and file-based requests to the eye backend
- Streams artifact downloads back to the frontend
- Handles CORS for the Vite frontend

## Routes

### Posture
- `POST /posture/predict` → `POST http://localhost:8001/predict`
- `POST /posture/predict-test` → `POST http://localhost:8001/predict-test`
- `POST /posture/analyze` → alias of `/posture/predict`
- `GET /posture/health` → `GET http://localhost:8001/health`

### Eye
- `POST /eye/analyze-session` → `POST http://localhost:8004/analyze-session`
- `POST /eye/predict` → alias of `/eye/analyze-session`
- `POST /eye/predict-from-features` → `POST http://localhost:8004/predict-from-features`
- `POST /eye/predict-from-session-files` → `POST http://localhost:8004/predict-from-session-files`
- `GET /eye/runs/{run_id}/download` → `GET http://localhost:8004/runs/{run_id}/download`
- `GET /eye/health` → `GET http://localhost:8004/health`

## Install

```bash
pip install -r requirements.txt
```

## Run

```bashs
uvicorn app.main:app --reload --port 8000
```

## Optional environment variables

```env
BODY_POSTURE_BASE_URL=http://localhost:8001
EYE_TRACKING_BASE_URL=http://localhost:8004
REQUEST_TIMEOUT_SECONDS=300
CORS_ORIGINS=["http://localhost:5173"]
```

## Notes

- The current posture backend accepts multipart video uploads, not JSON feature payloads.
- The current eye backend is HTTP-based in this codebase; the old frontend WebSocket helper is not wired to a live backend route.
