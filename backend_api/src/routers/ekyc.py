from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.security.deps import get_current_user
from src.services.ekyc_service import EKYCService

router = APIRouter()


class EKYCInitiateResponse(BaseModel):
    provider_ref: str = Field(..., description="Reference ID at eKYC provider")
    status: str = Field(..., description="Initial status")


@router.post("/initiate", summary="Initiate eKYC", response_model=EKYCInitiateResponse)
def initiate(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Initiate a mock eKYC process and return provider reference.
    """
    svc = EKYCService(db)
    try:
        provider_ref, record = svc.initiate(user_id=user.id)
        return EKYCInitiateResponse(provider_ref=provider_ref, status=record.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


class EKYCWebhookPayload(BaseModel):
    provider_ref: str = Field(..., description="Reference returned by initiate")
    status: str = Field(..., description="approved or rejected")
    details: Dict[str, Any] | None = Field(default=None, description="Additional details")


@router.post("/webhook", summary="eKYC Webhook")
def webhook(payload: EKYCWebhookPayload, x_ekyc_signature: str = Header(default=""), db: Session = Depends(get_db)):
    """
    eKYC webhook endpoint. Validates signature and updates record status.

    Header:
    - X-EKYC-Signature: HMAC signature of the payload.
    """
    svc = EKYCService(db)
    try:
        record = svc.handle_webhook(payload.dict(), signature=x_ekyc_signature)
        return {"status": record.status}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
