from __future__ import annotations

from typing import Tuple

from sqlalchemy.orm import Session

from src.repositories.user_repo import UserRepository
from src.security.crypto import hash_password, verify_password, create_access_token, create_refresh_token
from src.models.models import User


class AuthService:
    """Service for authentication and user registration."""

    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    # PUBLIC_INTERFACE
    def register_user(self, email: str, password: str, is_admin: bool = False) -> User:
        """Register new user if email not taken."""
        existing = self.users.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")
        hashed = hash_password(password)
        return self.users.create(email=email, hashed_password=hashed, is_admin=is_admin)

    # PUBLIC_INTERFACE
    def authenticate(self, email: str, password: str) -> Tuple[str, str, User]:
        """Authenticate a user and return (access_token, refresh_token, user)."""
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        access = create_access_token(subject=str(user.id))
        refresh = create_refresh_token(subject=str(user.id))
        return access, refresh, user
