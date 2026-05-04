from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .security import decode_access_token
from .db import db

bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user = await db.user.find_unique(where={"id": int(payload["sub"])})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if user.status == "REJECTED":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account rejected")
    return {"user": user, "role": payload.get("role")}

def require_roles(*allowed_roles: str):
    async def inner(current=Depends(get_current_user)):
        role = current.get("role")
        if role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return current
    return inner

require_admin = require_roles("ADMIN")
require_doctor = require_roles("DOCTOR")
require_parent = require_roles("PATIENT_PARENT")
require_guest = require_roles("GUEST")
