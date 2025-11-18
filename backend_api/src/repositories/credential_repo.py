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
        # No return value required
```

Explanation: Sharing repository.
````write file="secure-credential-wallet-40962-40972/backend_api/src/repositories/sharing_repo.py"
from __future__ import annotations

import secrets
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session

from src.models.models import Share


class SharingRepository:
    """Repository for credential sharing operations."""

    def __init__(self, db: Session):
        self.db = db

    # PUBLIC_INTERFACE
    def create_share(
        self, credential_id: int, shared_with_email: str, validity_seconds: int = 86400
    ) -> Share:
        """Create a share token for a credential."""
        token = secrets.token_urlsafe(24)
        expires_at = datetime.utcnow() + timedelta(seconds=validity_seconds)
        share = Share(
            credential_id=credential_id, shared_with_email=shared_with_email, token=token, expires_at=expires_at
        )
        self.db.add(share)
        self.db.flush()
        return share

    # PUBLIC_INTERFACE
    def get_by_token(self, token: str) -> Optional[Share]:
        """Retrieve share by its token."""
        return self.db.query(Share).filter(Share.token == token).first()

    # PUBLIC_INTERFACE
    def list_for_credential(self, credential_id: int) -> List[Share]:
        """List shares for a credential."""
        return self.db.query(Share).filter(Share.credential_id == credential_id).all()

    # PUBLIC_INTERFACE
    def delete(self, share: Share) -> None:
        """Delete a share entry."""
        self.db.delete(share)
