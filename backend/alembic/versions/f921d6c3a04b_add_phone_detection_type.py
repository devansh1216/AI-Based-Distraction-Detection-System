"""add phone detection event types

Revision ID: f921d6c3a04b
Revises: 2463a697debd
Create Date: 2026-11-22
"""
from typing import Sequence, Union

from alembic import op


revision: str = "f921d6c3a04b"
down_revision: Union[str, Sequence[str], None] = "2463a697debd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        op.execute("ALTER TYPE behaviour_type ADD VALUE IF NOT EXISTS 'PHONE_DETECTED'")
        op.execute("ALTER TYPE alert_type ADD VALUE IF NOT EXISTS 'PHONE_DETECTED'")


def downgrade() -> None:
    if op.get_bind().dialect.name == "postgresql":
        raise RuntimeError("PostgreSQL enum values cannot be removed safely.")
