from __future__ import annotations

from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_default_admin(db: Session) -> None:
    from app.models import User, UserRole, UserStatus
    from app.security import hash_password

    admin_email = "adminadhd@gmail.com"
    admin = db.scalar(select(User).where(User.email == admin_email))
    if admin:
        return

    db.add(
        User(
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            email=admin_email,
            full_name="Default Admin",
            password_hash=hash_password("Test@1234"),
        )
    )
    db.commit()


def init_db() -> None:
    Path(__file__).resolve().parents[1].joinpath("uploads").mkdir(parents=True, exist_ok=True)
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_default_admin(db)