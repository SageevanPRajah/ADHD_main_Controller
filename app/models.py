from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    PATIENT_PARENT = "PATIENT_PARENT"
    GUEST = "GUEST"


class UserStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole, native_enum=False), index=True, nullable=False)
    status: Mapped[UserStatus] = mapped_column(
        SAEnum(UserStatus, native_enum=False),
        index=True,
        nullable=False,
        default=UserStatus.PENDING,
    )
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    medical_council_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    parent_id: Mapped[str | None] = mapped_column(String(100), unique=True, index=True, nullable=True)
    google_sub: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hospital: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    child_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    child_age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    certificate_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    certificate_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    picture_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    doctor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    doctor: Mapped["User | None"] = relationship("User", remote_side=[id], back_populates="patients")
    patients: Mapped[list["User"]] = relationship(
        "User",
        back_populates="doctor",
        foreign_keys="User.doctor_id",
    )