from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.services.auth_service import AuthService

router = APIRouter()


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


@router.post("/register", summary="Register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user and return tokens.
    """
    svc = AuthService(db)
    try:
        svc.register_user(payload.email, payload.password)
        access, refresh, _ = svc.authenticate(payload.email, payload.password)
        return TokenResponse(access_token=access, refresh_token=refresh)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Password")


@router.post("/login", summary="Login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password, return access and refresh tokens.
    """
    svc = AuthService(db)
    try:
        access, refresh, _ = svc.authenticate(payload.email, payload.password)
        return TokenResponse(access_token=access, refresh_token=refresh)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
