"""
PUBLIC_INTERFACE
Run database migrations using Alembic programmatically.

Example:
    python -m scripts.migrate
"""
from __future__ import annotations

from alembic import command
from alembic.config import Config
from pathlib import Path


def main() -> None:
    """Run upgrade head."""
    cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    command.upgrade(cfg, "head")


if __name__ == "__main__":
    main()
