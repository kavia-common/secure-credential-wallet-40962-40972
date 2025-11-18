from __future__ import annotations

import datetime as dt
import secrets
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.models import Share


class SharingRepository:
    """Repository for managing Share persistence operations."""

    def __init__(self, db: Session):
        self.db = db

    # PUBLIC_INTERFACE
    def create_share(
        self,
        credential_id: int,
        shared_with_email: str,
        validity_seconds: int = 86400,
    ) -> Share:
        """
        Create a new Share entry.

        - Generates a random token (urlsafe).
        - Sets expires_at to now + validity_seconds (if validity_seconds > 0); otherwise None.
        - Enforces unique constraint on (credential_id, shared_with_email).

        Raises:
            ValueError: On duplicate (credential_id, shared_with_email) or other integrity errors.
        """
        token = secrets.token_urlsafe(24)
        expires_at: dt.datetime | None = None
        if validity_seconds and validity_seconds > 0:
            expires_at = dt.datetime.utcnow() + dt.timedelta(seconds=validity_seconds)

        share = Share(
            credential_id=credential_id,
            shared_with_email=shared_with_email,
            token=token,
            expires_at=expires_at,
        )
        self.db.add(share)
        try:
            # flush to get id and catch integrity errors early
            self.db.flush()
        except IntegrityError:
            # rollback the failed state so future operations continue
            self.db.rollback()
            raise ValueError("Share already exists for this recipient")
        return share

    # PUBLIC_INTERFACE
    def get_by_token(self, token: str) -> Optional[Share]:
        """
        Retrieve a Share by its token.
        """
        return self.db.query(Share).filter(Share.token == token).first()

    # PUBLIC_INTERFACE
    def get_share_by_token_hash(self, token: str) -> Optional[Share]:
        """
        Legacy/helper alias for compatibility if service expects a hash-based name.
        Here it simply delegates to get_by_token (no hashing stored in DB).
        """
        return self.get_by_token(token)

    # PUBLIC_INTERFACE
    def list_for_credential(self, credential_id: int) -> List[Share]:
        """
        List all shares associated with a credential, newest first.
        """
        return (
            self.db.query(Share)
            .filter(Share.credential_id == credential_id)
            .order_by(Share.created_at.desc())
            .all()
        )

    # PUBLIC_INTERFACE
    def revoke_share(self, share: Share) -> None:
        """
        Revoke a given share (delete it).
        """
        self.db.delete(share)

    # PUBLIC_INTERFACE
    def revoke_by_recipient(self, credential_id: int, shared_with_email: str) -> int:
        """
        Convenience method to revoke a share for a specific recipient.
        Returns the number of rows deleted.
        """
        q = self.db.query(Share).filter(
            and_(Share.credential_id == credential_id, Share.shared_with_email == shared_with_email)
        )
        count = 0
        for s in q.all():
            self.db.delete(s)
            count += 1
        if count:
            self.db.flush()
        return count
