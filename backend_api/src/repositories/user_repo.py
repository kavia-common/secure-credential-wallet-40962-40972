from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.models.models import User


class UserRepository:
    """Repository for user persistence operations."""

    def __init__(self, db: Session):
        self.db = db

    # PUBLIC_INTERFACE
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    # PUBLIC_INTERFACE
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by id."""
        return self.db.query(User).filter(User.id == user_id).first()

    # PUBLIC_INTERFACE
    def create(self, email: str, hashed_password: str, is_admin: bool = False) -> User:
        """Create a new user."""
        user = User(email=email, hashed_password=hashed_password, is_admin=is_admin)
        self.db.add(user)
        self.db.flush()
        return user
