from __future__ import annotations

from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.models import Credential


class CredentialRepository:
    """Repository for credential persistence operations."""

    def __init__(self, db: Session):
        self.db = db

    # PUBLIC_INTERFACE
    def create(self, owner_id: int, title: str, encrypted_blob: str) -> Credential:
        """Create new credential."""
        cred = Credential(owner_id=owner_id, title=title, encrypted_blob=encrypted_blob)
        self.db.add(cred)
        self.db.flush()
        return cred

    # PUBLIC_INTERFACE
    def get(self, cred_id: int, owner_id: int) -> Optional[Credential]:
        """Get credential by id for owner."""
        return (
            self.db.query(Credential)
            .filter(Credential.id == cred_id, Credential.owner_id == owner_id)
            .first()
        )

    # PUBLIC_INTERFACE
    def list_for_owner(self, owner_id: int) -> List[Credential]:
        """List credentials for owner."""
        return (
            self.db.query(Credential)
            .filter(Credential.owner_id == owner_id)
            .order_by(Credential.created_at.desc())
            .all()
        )

    # PUBLIC_INTERFACE
    def update_blob(self, cred: Credential, encrypted_blob: str) -> Credential:
        """Update credential encrypted blob."""
        cred.encrypted_blob = encrypted_blob
        self.db.add(cred)
        self.db.flush()
        return cred

    # PUBLIC_INTERFACE
    def delete(self, cred: Credential) -> None:
        """Delete credential."""
        self.db.delete(cred)
