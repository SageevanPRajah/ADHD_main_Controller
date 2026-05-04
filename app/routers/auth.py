from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas
from app.db import db
from app.security import verify_password, create_access_token, hash_password
from app.dependencies import get_current_user
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

router = APIRouter(prefix="/auth", tags=["auth"]) 

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")


@router.post("/admin/login", response_model=schemas.TokenResponse)
async def admin_login(payload: schemas.AdminLoginRequest):
    user = await db.user.find_unique(where={"email": payload.email})
    if not user or user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not verify_password(payload.password, user.passwordHash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.id, user.role)
    return {"access_token": token, "user": user.model_dump()}


@router.post("/doctor/request")
async def doctor_request(payload: schemas.DoctorRequest):
    # create doctor with PENDING status
    created = await db.user.create(
        data={
            "role": "DOCTOR",
            "status": "PENDING",
            "fullName": payload.full_name,
            "medicalCouncilId": payload.medical_council_id,
            "specialization": payload.specialization,
            "hospital": payload.hospital,
            "phoneNumber": payload.phone_number,
            "notes": payload.notes,
        }
    )
    return {"message": "Doctor request submitted", "doctor_id": created.id}


@router.post("/doctor/login", response_model=schemas.TokenResponse)
async def doctor_login(payload: schemas.DoctorLoginRequest):
    user = await db.user.find_unique(where={"medicalCouncilId": payload.medical_council_id})
    if not user or user.role != "DOCTOR" or user.status != "ACTIVE":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or account not active")
    if not verify_password(payload.password, user.passwordHash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.id, user.role)
    return {"access_token": token, "user": user.model_dump()}


@router.post("/parent/login", response_model=schemas.TokenResponse)
async def parent_login(payload: schemas.ParentLoginRequest):
    user = await db.user.find_unique(where={"parentId": payload.parent_id})
    if not user or user.role != "PATIENT_PARENT" or user.status != "ACTIVE":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials or account not active")
    if not verify_password(payload.password, user.passwordHash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(user.id, user.role)
    return {"access_token": token, "user": user.model_dump()}


@router.post("/guest/google", response_model=schemas.TokenResponse)
async def guest_google(payload: schemas.GoogleLoginRequest):
    try:
        idinfo = id_token.verify_oauth2_token(payload.credential, google_requests.Request(), GOOGLE_CLIENT_ID) if GOOGLE_CLIENT_ID else id_token.verify_oauth2_token(payload.credential, google_requests.Request())
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid Google credential: {exc}")

    google_sub = idinfo.get("sub")
    email = idinfo.get("email")
    name = idinfo.get("name")
    picture = idinfo.get("picture")

    user = None
    if google_sub:
        user = await db.user.find_unique(where={"googleSub": google_sub})
    if not user and email:
        user = await db.user.find_unique(where={"email": email})

    if not user:
        user = await db.user.create(
            data={
                "role": "GUEST",
                "status": "ACTIVE",
                "googleSub": google_sub,
                "email": email,
                "fullName": name,
                "pictureUrl": picture,
            }
        )

    token = create_access_token(user.id, user.role)
    return {"access_token": token, "user": user.model_dump()}


@router.get("/me")
async def me(current=Depends(get_current_user)):
    return {"user": current.get("user"), "role": current.get("role")}
