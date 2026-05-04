from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class AdminLoginRequest(BaseModel):
    email: str
    password: str


class DoctorRequest(BaseModel):
    full_name: str
    medical_council_id: str
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    phone_number: Optional[str] = None
    notes: Optional[str] = None


class DoctorLoginRequest(BaseModel):
    medical_council_id: str
    password: str


class ParentLoginRequest(BaseModel):
    parent_id: str
    password: str


class GoogleLoginRequest(BaseModel):
    credential: str


class UserResponse(BaseModel):
    id: int
    role: str
    status: str
    email: Optional[str] = None
    fullName: Optional[str] = None
    parentId: Optional[str] = None
    medicalCouncilId: Optional[str] = None
    phoneNumber: Optional[str] = None
    specialization: Optional[str] = None
    hospital: Optional[str] = None
    notes: Optional[str] = None
    pictureUrl: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
