from __future__ import annotations

import hmac
import hashlib
import json
import secrets
from typing import Dict, Tuple

from sqlalchemy.orm import Session

from src.repositories.ekyc_repo import EKYCRepository
from src.models.models import EKYCRecord
from src.config.settings import settings


class EKYCService:
    """Service handling mock eKYC flow and webhooks."""

    def __init__(self, db: Session):
        self.db = db
        self.ekyc = EKYCRepository(db)

    # PUBLIC_INTERFACE
    def initiate(self, user_id: int) -> Tuple[str, EKYCRecord]:
        """Initiate a mock eKYC, returning a provider_ref and record."""
        if not settings.EKYC_PROVIDER_API_KEY:
            raise ValueError("EKYC provider not configured")
        provider_ref = f"ekyc_{secrets.token_hex(8)}"
        record = self.ekyc.create(user_id=user_id, provider_ref=provider_ref, status="pending")
        return provider_ref, record

    # PUBLIC_INTERFACE
    def verify_webhook(self, payload: Dict, signature: str) -> bool:
        """Verify webhook signature with shared secret."""
        if not settings.EKYC_WEBHOOK_SECRET:
            return False
        mac = hmac.new(
            settings.EKYC_WEBHOOK_SECRET.encode(),
            json.dumps(payload, sort_keys=True).encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(mac, signature)

    # PUBLIC_INTERFACE
    def handle_webhook(self, payload: Dict, signature: str) -> EKYCRecord:
        """Handle webhook: update record status based on payload."""
        if not self.verify_webhook(payload, signature):
            raise ValueError("Invalid signature")
        provider_ref = payload.get("provider_ref")
        status = payload.get("status")
        result_payload = json.dumps(payload)
        record = self.ekyc.get_by_provider_ref(provider_ref)
        if not record:
            raise ValueError("Record not found")
        if status not in {"approved", "rejected"}:
            raise ValueError("Invalid status")
        return self.ekyc.update_status(record, status=status, payload=result_payload)
