from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.services.proxy_helpers import forward_json


async def proxy_handwriting_predict(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_json(request, f"{settings.handwriting_base_url}/handwriting/predict")


async def proxy_handwriting_analyze(request: Request) -> JSONResponse:
    content_type = request.headers.get('content-type', '').lower()

    # Current handwriting backend only supports JSON stroke/session payloads.
    # Keep a gateway endpoint for future multipart support, but fail clearly for now.
    if 'multipart/form-data' in content_type:
        raise HTTPException(
            status_code=501,
            detail=(
                'Current handwriting backend does not expose a file-upload endpoint. '
                'Use JSON stroke/session analysis through /handwriting/predict.'
            ),
        )

    return await proxy_handwriting_predict(request)
