from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from config import get_settings
from services.proxy_helpers import forward_form_with_files


async def proxy_voice_analyze(request: Request) -> JSONResponse:
    settings = get_settings()
    return await forward_form_with_files(request, f"{settings.voice_analysis_base_url}/analyze")
