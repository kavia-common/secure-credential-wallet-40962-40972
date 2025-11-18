from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.repositories.user_repo import UserRepository
from src.security.crypto import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Retrieve current user from JWT access token."""
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise ValueError("Invalid token")
        user = UserRepository(db).get_by_id(int(sub))
        if not user or not user.is_active:
            raise ValueError("Inactive or missing user")
        return user
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


# PUBLIC_INTERFACE
def require_admin(user=Depends(get_current_user)):
    """Ensure the current user is admin."""
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin required")
    return user
