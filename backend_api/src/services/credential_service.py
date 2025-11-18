from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from src.repositories.credential_repo import CredentialRepository
from src.security.crypto import encrypt_text, decrypt_text
from src.models.models import Credential


class CredentialService:
    """Service for encrypted credential storage."""

    def __init__(self, db: Session):
        self.db = db
        self.creds = CredentialRepository(db)

    # PUBLIC_INTERFACE
    def create(self, owner_id: int, title: str, plain_text: str) -> Credential:
        """Create a credential with encrypted content."""
        blob = encrypt_text(plain_text)
        return self.creds.create(owner_id=owner_id, title=title, encrypted_blob=blob)

    # PUBLIC_INTERFACE
    def get_plain(self, cred_id: int, owner_id: int) -> str:
        """Retrieve and decrypt credential text."""
        cred = self.creds.get(cred_id, owner_id)
        if not cred:
            raise ValueError("Not found")
        return decrypt_text(cred.encrypted_blob)

    # PUBLIC_INTERFACE
    def list_for_owner(self, owner_id: int) -> List[Credential]:
        """List credentials for owner."""
        return self.creds.list_for_owner(owner_id)

    # PUBLIC_INTERFACE
    def update(self, cred_id: int, owner_id: int, new_plain_text: str) -> Credential:
        """Update credential content."""
        cred = self.creds.get(cred_id, owner_id)
        if not cred:
            raise ValueError("Not found")
        blob = encrypt_text(new_plain_text)
        return self.creds.update_blob(cred, blob)

    # PUBLIC_INTERFACE
    def delete(self, cred_id: int, owner_id: int) -> None:
        """Delete a credential."""
        cred = self.creds.get(cred_id, owner_id)
        if not cred:
            raise ValueError("Not found")
        self.creds.delete(cred)
