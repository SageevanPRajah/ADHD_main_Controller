from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.services.proxy_helpers import forward_form_with_files


async def proxy_posture_predict(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_form_with_files(request, f"{settings.body_posture_base_url}/predict")


async def proxy_posture_predict_test(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_form_with_files(request, f"{settings.body_posture_base_url}/predict-test")
