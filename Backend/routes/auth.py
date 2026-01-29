from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Dict

from Backend.schemas import AdminLoginPayload

from .database import get_db
from .models import User

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/admin/login")
def admin_login(payload: AdminLoginPayload, db: Session = Depends(get_db)):
    email = payload.email
    password = payload.password

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user: User | None = (
        db.query(User)
        .filter(
            User.email == email,
            User.role == "admin",
            User.is_active.is_( True)
        )
        .first()
    )

    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not pwd_context.verify(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {
        "status": "ok",  
        "admin_id": user.id,
        "name": user.name
    }

# import bcrypt
# from fastapi import APIRouter, HTTPException
# from passlib.context import CryptContext
# import os
# from ..config.admin import ADMIN_EMAIL, ADMIN_PASSWORD

# router = APIRouter(prefix="/auth", tags=["Auth"])
# pwd = CryptContext(schemes=["bcrypt"])

# @router.post("/login")
# def admin_login(data: dict):
#     email = data["email"]
#     password = data["password"]

#     if email != os.getenv("ADMIN_EMAIL"):
#         raise HTTPException(401, "Invalid credentials")

#     if not pwd.verify(password, os.getenv("ADMIN_PASSWORD_HASH")):
#         raise HTTPException(401, "Invalid credentials")

#     return {"status": "ok"}