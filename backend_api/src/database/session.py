from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.config.settings import settings

_engine = None
_SessionLocal: Optional[sessionmaker] = None


def init_engine_and_session() -> None:
    """Initialize SQLAlchemy engine and session factory."""
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(settings.DB_URL, pool_pre_ping=True, future=True)
        _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False, future=True)


def close_engine() -> None:
    """Dispose engine on shutdown."""
    global _engine
    if _engine is not None:
        _engine.dispose()
        _engine = None


# PUBLIC_INTERFACE
@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    if _SessionLocal is None:
        init_engine_and_session()
    assert _SessionLocal is not None
    db = _SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


# PUBLIC_INTERFACE
def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session."""
    with session_scope() as db:
        yield db
