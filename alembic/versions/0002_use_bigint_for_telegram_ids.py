"""use bigint for telegram ids

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-15
"""

from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("users", "telegram_id", existing_type=sa.Integer(), type_=sa.BigInteger(), existing_nullable=True)


def downgrade() -> None:
    op.alter_column("users", "telegram_id", existing_type=sa.BigInteger(), type_=sa.Integer(), existing_nullable=True)
