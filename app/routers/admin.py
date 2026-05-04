from fastapi import APIRouter, Depends, HTTPException, status
from app.db import db
from app.dependencies import require_admin
from app.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"]) 


@router.get("/doctors/pending")
async def get_pending_doctors(_=Depends(require_admin)):
    doctors = await db.user.find_many(where={"role": "DOCTOR", "status": "PENDING"})
    return doctors


@router.get("/doctors")
async def get_all_doctors(_=Depends(require_admin)):
    doctors = await db.user.find_many(where={"role": "DOCTOR"})
    return doctors


@router.post("/doctors/{doctor_id}/approve")
async def approve_doctor(doctor_id: int, _=Depends(require_admin)):
    doctor = await db.user.find_unique(where={"id": doctor_id})
    if not doctor or doctor.role != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    await db.user.update(where={"id": doctor_id}, data={"status": "ACTIVE", "passwordHash": hash_password("TestD@1234")})
    return {"message": "Doctor approved successfully. Default password is TestD@1234"}


@router.post("/doctors/{doctor_id}/reject")
async def reject_doctor(doctor_id: int, _=Depends(require_admin)):
    doctor = await db.user.find_unique(where={"id": doctor_id})
    if not doctor or doctor.role != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    await db.user.update(where={"id": doctor_id}, data={"status": "REJECTED"})
    return {"message": "Doctor rejected"}
from fastapi import APIRouter, Depends, HTTPException, status
from app.db import db
from app.dependencies import require_admin
from app.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"]) 


@router.get("/doctors/pending")
async def get_pending_doctors(_=Depends(require_admin)):
    doctors = await db.user.find_many(where={"role": "DOCTOR", "status": "PENDING"})
    return doctors


@router.get("/doctors")
async def get_all_doctors(_=Depends(require_admin)):
    doctors = await db.user.find_many(where={"role": "DOCTOR"})
    return doctors


@router.post("/doctors/{doctor_id}/approve")
async def approve_doctor(doctor_id: int, _=Depends(require_admin)):
    doctor = await db.user.find_unique(where={"id": doctor_id})
    if not doctor or doctor.role != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    await db.user.update(where={"id": doctor_id}, data={"status": "ACTIVE", "passwordHash": hash_password("TestD@1234")})
    return {"message": "Doctor approved successfully. Default password is TestD@1234"}


@router.post("/doctors/{doctor_id}/reject")
async def reject_doctor(doctor_id: int, _=Depends(require_admin)):
    doctor = await db.user.find_unique(where={"id": doctor_id})
    if not doctor or doctor.role != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    await db.user.update(where={"id": doctor_id}, data={"status": "REJECTED"})
    return {"message": "Doctor rejected"}