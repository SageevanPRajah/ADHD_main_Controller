from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers.eye import router as eye_router
from app.routers.handwriting import router as handwriting_router
from app.routers.posture import router as posture_router
from app.routers.voice import router as voice_router

settings = get_settings()

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def root():
    return {
        'name': settings.app_name,
        'version': settings.app_version,
        'routes': {
            'posture': ['/posture/predict', '/posture/predict-test', '/posture/analyze'],
            'eye': [
                '/eye/analyze-session',
                '/eye/predict',
                '/eye/predict-from-features',
                '/eye/predict-from-session-files',
                '/eye/runs/{run_id}/download',
            ],
            'voice': ['/voice/analyze'],
            'handwriting': ['/handwriting/predict', '/handwriting/analyze', '/handwriting/health'],
        },
        'downstream_services': {
            'posture': settings.body_posture_base_url,
            'eye': settings.eye_tracking_base_url,
            'voice': settings.voice_analysis_base_url,
            'handwriting': settings.handwriting_base_url,
        },
    }


@app.get('/health')
async def health():
    return {
        'ok': True,
        'gateway': True,
        'services': {
            'posture': settings.body_posture_base_url,
            'eye': settings.eye_tracking_base_url,
            'voice': settings.voice_analysis_base_url,
            'handwriting': settings.handwriting_base_url,
        },
    }


app.include_router(posture_router)
app.include_router(eye_router)
app.include_router(voice_router)
app.include_router(handwriting_router)
