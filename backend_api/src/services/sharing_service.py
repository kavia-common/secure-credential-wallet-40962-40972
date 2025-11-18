from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from src.repositories.credential_repo import CredentialRepository
from src.repositories.sharing_repo import SharingRepository
from src.security.crypto import decrypt_text
from src.models.models import Share


class SharingService:
    """Service to manage credential sharing tokens."""

    def __init__(self, db: Session):
        self.db = db
        self.creds = CredentialRepository(db)
        self.shares = SharingRepository(db)

    # PUBLIC_INTERFACE
    def create_share(
        self,
        owner_id: int,
        credential_id: int,
        email: str,
        validity_seconds: int = 86400,
    ) -> Share:
        """Create a share entry if credential belongs to owner."""
        cred = self.creds.get(credential_id, owner_id)
        if not cred:
            raise ValueError("Credential not found")
        return self.shares.create_share(
            credential_id=credential_id,
            shared_with_email=email,
            validity_seconds=validity_seconds,
        )

    # PUBLIC_INTERFACE
    def access_shared(self, token: str) -> str:
        """Return decrypted credential text by share token."""
        share = self.shares.get_by_token(token)
        if not share:
            raise ValueError("Invalid token")
        if share.expires_at is not None and share.expires_at < __import__("datetime").datetime.utcnow():
            raise ValueError("Token expired")
        # Fallback using Session.get for SQLAlchemy 2.0
        from src.models.models import Credential as CredModel
        cred = self.db.get(CredModel, share.credential_id)
        if not cred:
            raise ValueError("Credential missing")
        return decrypt_text(cred.encrypted_blob)

    # PUBLIC_INTERFACE
    def list_shares(self, credential_id: int) -> List[Share]:
        """List shares for a credential."""
        return self.shares.list_for_credential(credential_id)
