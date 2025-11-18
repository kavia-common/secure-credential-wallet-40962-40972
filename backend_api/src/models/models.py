from __future__ import annotations

import datetime as dt

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database.base import Base


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)

    credentials: Mapped[list["Credential"]] = relationship("Credential", back_populates="owner", cascade="all,delete")
    ekyc_records: Mapped[list["EKYCRecord"]] = relationship("EKYCRecord", back_populates="user", cascade="all,delete")


class Credential(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    encrypted_blob: Mapped[str] = mapped_column(Text, nullable=False)  # base64(salt+nonce+ciphertext+mac)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )

    owner: Mapped["User"] = relationship("User", back_populates="credentials")
    shares: Mapped[list["Share"]] = relationship("Share", back_populates="credential", cascade="all,delete")


class Share(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    credential_id: Mapped[int] = mapped_column(
        ForeignKey("credential.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    shared_with_email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)

    credential: Mapped["Credential"] = relationship("Credential", back_populates="shares")

    __table_args__ = (UniqueConstraint("credential_id", "shared_with_email", name="uq_credential_email"),)


class EKYCRecord(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)  # pending/approved/rejected
    provider_ref: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    result_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="ekyc_records")
