from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import connect_db, disconnect_db, db
from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.doctor_accounts import router as doctor_accounts_router
from app.routers.eye import router as eye_router
from app.routers.handwriting import router as handwriting_router
from app.routers.parent_accounts import router as parent_accounts_router
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


@app.on_event('startup')
async def startup_event() -> None:
    # connect Prisma client and seed default admin
    await connect_db()
    # seed default admin if not exists
    from app.security import hash_password

    admin_email = "adminadhd@gmail.com"
    existing = await db.user.find_unique(where={"email": admin_email})
    if not existing:
        await db.user.create(
            data={
                "role": "ADMIN",
                "status": "ACTIVE",
                "email": admin_email,
                "fullName": "Default Admin",
                "passwordHash": hash_password("Test@1234"),
            }
        )


@app.on_event('shutdown')
async def shutdown_event() -> None:
    await disconnect_db()


@app.get('/')
async def root():
    return {
        'name': settings.app_name,
        'version': settings.app_version,
        'routes': {
            'auth': ['/auth/admin/login', '/auth/doctor/request', '/auth/doctor/login', '/auth/parent/login', '/auth/guest/google', '/auth/me'],
            'admin': ['/admin/doctors/pending', '/admin/doctors', '/admin/doctors/{doctor_id}/approve', '/admin/doctors/{doctor_id}/reject'],
            'doctor': ['/doctor/patients', '/doctor/patients/{parent_id}'],
            'parent': ['/parent/me'],
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
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(doctor_accounts_router)
app.include_router(parent_accounts_router)
