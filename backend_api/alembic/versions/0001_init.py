from __future__ import annotations

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "credential",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "owner_id",
            sa.Integer(),
            sa.ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("encrypted_blob", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "share",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "credential_id",
            sa.Integer(),
            sa.ForeignKey("credential.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("shared_with_email", sa.String(length=255), nullable=False, index=True),
        sa.Column("token", sa.String(length=255), nullable=False, unique=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.UniqueConstraint("credential_id", "shared_with_email", name="uq_credential_email"),
    )

    op.create_table(
        "ekycrecord",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("provider_ref", sa.String(length=255), nullable=False, unique=True),
        sa.Column("result_payload", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("ekycrecord")
    op.drop_table("share")
    op.drop_table("credential")
    op.drop_table("user")
