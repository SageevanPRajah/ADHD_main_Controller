from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.services.handwriting_service import proxy_handwriting_analyze, proxy_handwriting_predict

router = APIRouter(prefix='/handwriting', tags=['handwriting'])


@router.get('/health')
async def handwriting_health() -> JSONResponse:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(settings.request_timeout_seconds)) as client:
            response = await client.get(f"{settings.handwriting_base_url}/health")
        return JSONResponse(status_code=response.status_code, content=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f'Handwriting service unavailable: {exc}') from exc


@router.post('/predict')
async def handwriting_predict(request: Request) -> JSONResponse:
    return await proxy_handwriting_predict(request)


@router.post('/analyze')
async def handwriting_analyze(request: Request) -> JSONResponse:
    return await proxy_handwriting_analyze(request)
