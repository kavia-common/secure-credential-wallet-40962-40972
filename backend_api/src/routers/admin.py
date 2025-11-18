from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.security.deps import require_admin
from src.models.models import User

router = APIRouter()


class UserOut(BaseModel):
    id: int
    email: str
    is_admin: bool
    is_active: bool

    class Config:
        from_attributes = True


@router.get("/users", summary="List Users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    """
    List all users (admin only).
    """
    users = db.query(User).order_by(User.created_at.desc()).all()
    return users


@router.post("/users/{user_id}/promote", summary="Promote to Admin")
def promote_user(user_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    """
    Promote user to admin.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    db.add(user)
    db.commit()
    return {"status": "promoted", "user_id": user.id}
