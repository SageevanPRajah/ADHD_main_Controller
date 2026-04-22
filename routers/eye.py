from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from config import get_settings
from services.eye_service import (
    proxy_eye_analyze_session,
    proxy_eye_download_run,
    proxy_eye_predict_from_features,
    proxy_eye_predict_from_session_files,
)

router = APIRouter(prefix='/eye', tags=['eye'])


@router.get('/health')
async def eye_health() -> JSONResponse:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(settings.request_timeout_seconds)) as client:
            response = await client.get(f"{settings.eye_tracking_base_url}/health")
        return JSONResponse(status_code=response.status_code, content=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f'Eye service unavailable: {exc}') from exc


@router.post('/analyze-session')
async def eye_analyze_session(request: Request) -> JSONResponse:
    return await proxy_eye_analyze_session(request)


@router.post('/predict')
async def eye_predict_alias(request: Request) -> JSONResponse:
    return await proxy_eye_analyze_session(request)


@router.post('/predict-from-features')
async def eye_predict_from_features(request: Request) -> JSONResponse:
    return await proxy_eye_predict_from_features(request)


@router.post('/predict-from-session-files')
async def eye_predict_from_session_files(request: Request) -> JSONResponse:
    return await proxy_eye_predict_from_session_files(request)


@router.get('/runs/{run_id}/download')
async def eye_download_run(request: Request, run_id: str) -> StreamingResponse:
    return await proxy_eye_download_run(request, run_id)
