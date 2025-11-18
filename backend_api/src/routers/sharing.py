from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.security.deps import get_current_user
from src.services.sharing_service import SharingService

router = APIRouter()


class ShareCreate(BaseModel):
    credential_id: int = Field(..., description="Credential ID to share")
    email: EmailStr = Field(..., description="Recipient email")
    validity_seconds: int = Field(default=86400, description="Validity in seconds")


class ShareOut(BaseModel):
    id: int
    credential_id: int
    shared_with_email: str
    token: str

    class Config:
        from_attributes = True


class SharedAccessResponse(BaseModel):
    content: str


@router.post("", summary="Create Share", response_model=ShareOut)
def create_share(payload: ShareCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Create a share token for a credential owned by the current user.
    """
    svc = SharingService(db)
    try:
        share = svc.create_share(
            owner_id=user.id,
            credential_id=payload.credential_id,
            email=payload.email,
            validity_seconds=payload.validity_seconds,
        )
        return share
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/access/{token}", summary="Access Shared Credential", response_model=SharedAccessResponse)
def access_shared(token: str, db: Session = Depends(get_db)):
    """
    Access shared credential content using a share token.
    """
    svc = SharingService(db)
    try:
        content = svc.access_shared(token)
        return SharedAccessResponse(content=content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
