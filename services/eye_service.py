from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse

from config import get_settings
from services.proxy_helpers import forward_form_with_files, forward_json, forward_stream


async def proxy_eye_analyze_session(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_json(request, f"{settings.eye_tracking_base_url}/analyze-session")


async def proxy_eye_predict_from_features(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_form_with_files(request, f"{settings.eye_tracking_base_url}/predict-from-features")


async def proxy_eye_predict_from_session_files(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_form_with_files(request, f"{settings.eye_tracking_base_url}/predict-from-session-files")


async def proxy_eye_download_run(request: Request, run_id: str) -> StreamingResponse:
    settings = get_settings()
    return await forward_stream(request, f"{settings.eye_tracking_base_url}/runs/{run_id}/download")
