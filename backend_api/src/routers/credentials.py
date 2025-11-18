from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.security.deps import get_current_user
from src.services.credential_service import CredentialService

router = APIRouter()


class CredentialCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Credential title")
    content: str = Field(..., description="Sensitive content to encrypt")


class CredentialUpdate(BaseModel):
    content: str = Field(..., description="New content")


class CredentialOut(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


class CredentialDetailOut(BaseModel):
    id: int
    title: str
    content: str


@router.post("", summary="Create Credential", response_model=CredentialOut)
def create_credential(payload: CredentialCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Create a new encrypted credential.
    """
    svc = CredentialService(db)
    cred = svc.create(owner_id=user.id, title=payload.title, plain_text=payload.content)
    return cred


@router.get("", summary="List Credentials", response_model=List[CredentialOut])
def list_credentials(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    List credentials for current user (without content).
    """
    svc = CredentialService(db)
    creds = svc.list_for_owner(owner_id=user.id)
    return creds


@router.get("/{cred_id}", summary="Get Credential", response_model=CredentialDetailOut)
def get_credential(cred_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Get credential content (decrypted).
    """
    svc = CredentialService(db)
    try:
        content = svc.get_plain(cred_id=cred_id, owner_id=user.id)
        from src.repositories.credential_repo import CredentialRepository

        c = CredentialRepository(db).get(cred_id, user.id)
        if not c:
            raise HTTPException(status_code=404, detail="Not found")
        return CredentialDetailOut(id=c.id, title=c.title, content=content)
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")


@router.put("/{cred_id}", summary="Update Credential", response_model=CredentialOut)
def update_credential(
    cred_id: int,
    payload: CredentialUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Update credential content.
    """
    svc = CredentialService(db)
    try:
        cred = svc.update(cred_id=cred_id, owner_id=user.id, new_plain_text=payload.content)
        return cred
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")


@router.delete("/{cred_id}", summary="Delete Credential")
def delete_credential(cred_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Delete credential.
    """
    svc = CredentialService(db)
    try:
        svc.delete(cred_id=cred_id, owner_id=user.id)
        return {"status": "deleted"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Not found")
