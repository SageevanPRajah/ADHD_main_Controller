from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.services.posture_service import (
    proxy_posture_predict,
    proxy_posture_predict_features,
    proxy_posture_predict_test,
)

router = APIRouter(prefix='/posture', tags=['posture'])


@router.get('/health')
async def posture_health() -> JSONResponse:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(settings.request_timeout_seconds)) as client:
            response = await client.get(f"{settings.body_posture_base_url}/health")
        return JSONResponse(status_code=response.status_code, content=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f'Posture service unavailable: {exc}') from exc


@router.post('/predict-features')
async def posture_predict_features(request: Request) -> JSONResponse:
    return await proxy_posture_predict_features(request)


@router.post('/predict')
async def posture_predict(request: Request) -> JSONResponse:
    return await proxy_posture_predict(request)


@router.post('/predict-test')
async def posture_predict_test(request: Request) -> JSONResponse:
    return await proxy_posture_predict_test(request)


@router.post('/analyze')
async def posture_analyze_alias(request: Request) -> JSONResponse:
    return await proxy_posture_predict(request)


@router.post('/analyze-test')
async def posture_analyze_test_alias(request: Request) -> JSONResponse:
    return await proxy_posture_predict_test(request)
