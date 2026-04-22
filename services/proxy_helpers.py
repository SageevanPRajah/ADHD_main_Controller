from __future__ import annotations

from typing import Any, Dict, Iterable, Tuple

import httpx
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.background import BackgroundTask

from config import get_settings

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "host",
    "content-length",
}


def _filtered_headers(
    headers: Iterable[Tuple[str, str]],
    *,
    drop_content_type: bool = False,
) -> Dict[str, str]:
    blocked = set(HOP_BY_HOP_HEADERS)
    if drop_content_type:
        blocked.add("content-type")

    return {k: v for k, v in headers if k.lower() not in blocked}


async def _request(
    method: str,
    url: str,
    *,
    headers: Dict[str, str] | None = None,
    json_body: Any = None,
    data: Any = None,
    files: Any = None,
    params: Dict[str, Any] | None = None,
) -> httpx.Response:
    settings = get_settings()
    timeout = httpx.Timeout(settings.request_timeout_seconds)

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.request(
                method,
                url,
                headers=headers,
                json=json_body,
                data=data,
                files=files,
                params=params,
            )
            return response
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Downstream request failed: {exc}",
            ) from exc


async def forward_json(request: Request, target_url: str) -> JSONResponse:
    body = await request.json()

    response = await _request(
        request.method,
        target_url,
        headers=_filtered_headers(request.headers.items()),
        json_body=body,
        params=dict(request.query_params),
    )

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type.lower():
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
            headers=_filtered_headers(response.headers.items()),
        )

    return JSONResponse(
        status_code=response.status_code,
        content={"detail": response.text},
        headers=_filtered_headers(response.headers.items()),
    )


async def forward_form_with_files(request: Request, target_url: str) -> JSONResponse:
    form = await request.form()

    data: Dict[str, str] = {}
    files: Dict[str, Tuple[str, bytes, str]] = {}

    for key, value in form.multi_items():
        filename = getattr(value, "filename", None)

        if filename is not None:
            content = await value.read()
            files[key] = (
                filename,
                content,
                value.content_type or "application/octet-stream",
            )
        else:
            data[key] = str(value)

    response = await _request(
        request.method,
        target_url,
        headers=_filtered_headers(
            request.headers.items(),
            drop_content_type=True,
        ),
        data=data,
        files=files,
        params=dict(request.query_params),
    )

    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type.lower():
        return JSONResponse(
            status_code=response.status_code,
            content=response.json(),
            headers=_filtered_headers(response.headers.items()),
        )

    return JSONResponse(
        status_code=response.status_code,
        content={"detail": response.text},
        headers=_filtered_headers(response.headers.items()),
    )


async def forward_stream(request: Request, target_url: str) -> StreamingResponse:
    settings = get_settings()
    timeout = httpx.Timeout(settings.request_timeout_seconds)
    client = httpx.AsyncClient(timeout=timeout)

    try:
        downstream = await client.send(
            client.build_request(
                request.method,
                target_url,
                headers=_filtered_headers(request.headers.items()),
                params=dict(request.query_params),
            ),
            stream=True,
        )
    except httpx.RequestError as exc:
        await client.aclose()
        raise HTTPException(
            status_code=502,
            detail=f"Downstream streaming request failed: {exc}",
        ) from exc

    response_headers = _filtered_headers(downstream.headers.items())

    return StreamingResponse(
        downstream.aiter_bytes(),
        status_code=downstream.status_code,
        media_type=downstream.headers.get("content-type"),
        headers=response_headers,
        background=BackgroundTask(client.aclose),
    )