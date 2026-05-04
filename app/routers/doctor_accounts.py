from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import require_doctor, get_current_user
from app.db import db
from app.security import hash_password

router = APIRouter(prefix="/doctor", tags=["doctor"]) 


@router.post("/patients")
async def create_parent(payload: dict, current=Depends(get_current_user)):
    # only doctors
    if current.get("role") != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    doctor_user = current.get("user")
    # generate parent id
    # find max existing numeric suffix
    existing = await db.user.find_many(where={"parentId": {"startsWith": "P-"}})
    max_num = 1000
    for u in existing:
        try:
            part = u.parentId.split("-")[-1]
            n = int(part)
            if n > max_num:
                max_num = n
        except Exception:
            continue
    new_id = f"P-{max_num + 1}"
    created = await db.user.create(
        data={
            "role": "PATIENT_PARENT",
            "status": "ACTIVE",
            "fullName": payload.get("parent_name"),
            "parentId": new_id,
            "passwordHash": hash_password("TestP@1234"),
            "doctorId": doctor_user.id,
            "phoneNumber": payload.get("contact_number"),
            "notes": payload.get("notes"),
        }
    )
    return {"message": "Parent account created successfully", "parentId": created.parentId, "defaultPassword": "TestP@1234"}


@router.get("/patients")
async def list_patients(current=Depends(get_current_user)):
    if current.get("role") != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    doctor_user = current.get("user")
    patients = await db.user.find_many(where={"doctorId": doctor_user.id, "role": "PATIENT_PARENT"})
    return patients


@router.get("/patients/{parent_id}")
async def get_patient(parent_id: str, current=Depends(get_current_user)):
    if current.get("role") != "DOCTOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    doctor_user = current.get("user")
    patient = await db.user.find_unique(where={"parentId": parent_id})
    if not patient or patient.doctorId != doctor_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return patient
