from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from src.models.models import EKYCRecord


class EKYCRepository:
    """Repository for eKYC records."""

    def __init__(self, db: Session):
        self.db = db

    # PUBLIC_INTERFACE
    def create(self, user_id: int, provider_ref: str, status: str = "pending") -> EKYCRecord:
        """Create a new eKYC record."""
        rec = EKYCRecord(user_id=user_id, provider_ref=provider_ref, status=status)
        self.db.add(rec)
        self.db.flush()
        return rec

    # PUBLIC_INTERFACE
    def get_by_provider_ref(self, provider_ref: str) -> Optional[EKYCRecord]:
        """Get eKYC record by provider ref."""
        return self.db.query(EKYCRecord).filter(EKYCRecord.provider_ref == provider_ref).first()

    # PUBLIC_INTERFACE
    def update_status(self, record: EKYCRecord, status: str, payload: str | None = None) -> EKYCRecord:
        """Update eKYC record status and payload."""
        record.status = status
        if payload is not None:
            record.result_payload = payload
        self.db.add(record)
        self.db.flush()
        return record
