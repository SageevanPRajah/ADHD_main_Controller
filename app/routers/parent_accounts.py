from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies import require_parent, get_current_user
from app.db import db

router = APIRouter(prefix="/parent", tags=["parent"]) 


@router.get("/me")
async def parent_me(current=Depends(get_current_user)):
    if current.get("role") != "PATIENT_PARENT":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    user = current.get("user")
    # load assigned doctor if present
    doctor = None
    if user.doctorId:
        doctor = await db.user.find_unique(where={"id": user.doctorId})
    return {
        "parentId": user.parentId,
        "fullName": user.fullName,
        "childName": user.notes,
        "childAge": None,
        "phoneNumber": user.phoneNumber,
        "status": user.status,
        "doctor": doctor,
    }
