from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from config import get_settings
from services.voice_service import proxy_voice_analyze

router = APIRouter(prefix='/voice', tags=['voice'])


@router.get('/health')
async def voice_health() -> JSONResponse:
    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(settings.request_timeout_seconds)) as client:
            response = await client.get(f"{settings.voice_analysis_base_url}/health")
        return JSONResponse(status_code=response.status_code, content=response.json())
    except httpx.RequestError as exc:
        raise HTTPException(status_code=502, detail=f'Voice service unavailable: {exc}') from exc


@router.post('/analyze')
async def voice_analyze(request: Request) -> JSONResponse:
    return await proxy_voice_analyze(request)
