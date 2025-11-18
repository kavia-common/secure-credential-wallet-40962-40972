from __future__ import annotations

import base64
import hashlib
import hmac
import os
import time
from typing import Any, Dict, Optional, Tuple

from jose import jwt
from passlib.context import CryptContext

from src.config.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# PUBLIC_INTERFACE
def hash_password(password: str) -> str:
    """Hash a plaintext password with passlib context (bcrypt)."""
    return pwd_context.hash(password)


# PUBLIC_INTERFACE
def verify_password(plain: str, hashed: str) -> bool:
    """Verify a plaintext password matches the hashed password."""
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        return False


def _now_ts() -> int:
    return int(time.time())


def _jwt_sign(payload: Dict[str, Any], ttl_seconds: int) -> str:
    to_encode = payload.copy()
    to_encode["iat"] = _now_ts()
    to_encode["exp"] = _now_ts() + ttl_seconds
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return token


# PUBLIC_INTERFACE
def create_access_token(subject: str, claims: Optional[Dict[str, Any]] = None) -> str:
    """Create a signed JWT access token."""
    payload = {"sub": subject}
    if claims:
        payload.update(claims)
    return _jwt_sign(payload, settings.ACCESS_TOKEN_TTL)


# PUBLIC_INTERFACE
def create_refresh_token(subject: str, claims: Optional[Dict[str, Any]] = None) -> str:
    """Create a signed JWT refresh token."""
    payload = {"sub": subject, "scope": "refresh"}
    if claims:
        payload.update(claims)
    return _jwt_sign(payload, settings.REFRESH_TOKEN_TTL)


# PUBLIC_INTERFACE
def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token using HS256."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


def _derive_key(master: str, salt: bytes) -> bytes:
    # Use PBKDF2-HMAC-SHA256 for key derivation
    return hashlib.pbkdf2_hmac("sha256", master.encode("utf-8"), salt, 200_000, dklen=32)


# PUBLIC_INTERFACE
def encrypt_bytes(plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
    """
    Encrypt plaintext bytes using a simple stream XOR with HMAC for integrity (placeholder).

    Returns (salt, nonce, ciphertext||mac)
    """
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = _derive_key(settings.ENCRYPTION_MASTER_KEY or settings.SECRET_KEY, salt)
    stream_key = hashlib.sha256(key + nonce).digest()
    ct = bytes([b ^ stream_key[i % len(stream_key)] for i, b in enumerate(plaintext)])
    mac = hmac.new(key, nonce + ct, hashlib.sha256).digest()
    return salt, nonce, ct + mac


# PUBLIC_INTERFACE
def decrypt_bytes(salt: bytes, nonce: bytes, ciphertext_mac: bytes) -> bytes:
    """
    Decrypt bytes encrypted by encrypt_bytes and verify integrity.
    """
    key = _derive_key(settings.ENCRYPTION_MASTER_KEY or settings.SECRET_KEY, salt)
    ct, mac = ciphertext_mac[:-32], ciphertext_mac[-32:]
    expected = hmac.new(key, nonce + ct, hashlib.sha256).digest()
    if not hmac.compare_digest(expected, mac):
        raise ValueError("Integrity check failed")
    stream_key = hashlib.sha256(key + nonce).digest()
    pt = bytes([b ^ stream_key[i % len(stream_key)] for i, b in enumerate(ct)])
    return pt


# PUBLIC_INTERFACE
def encrypt_text(text: str) -> str:
    """Encrypt text and return base64 string containing salt|nonce|ciphertext."""
    b = text.encode("utf-8")
    salt, nonce, ct = encrypt_bytes(b)
    return base64.b64encode(salt + nonce + ct).decode("ascii")


# PUBLIC_INTERFACE
def decrypt_text(b64: str) -> str:
    """Decrypt base64 string and return plaintext string."""
    blob = base64.b64decode(b64.encode("ascii"))
    salt, nonce, ct = blob[:16], blob[16:28], blob[28:]
    pt = decrypt_bytes(salt, nonce, ct)
    return pt.decode("utf-8")
