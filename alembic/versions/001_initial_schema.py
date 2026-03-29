# Migración inicial: tablas accounts y transfer_records.
#
# Es idempotente: si las tablas ya existían (p. ej. por Base.metadata.create_all o pruebas
# anteriores), no vuelve a crearlas y Alembic puede marcar la revisión sin error 1050.

from __future__ import annotations

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if not inspector.has_table("accounts"):
        op.create_table(
            "accounts",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("owner", sa.String(length=100), nullable=False),
            sa.Column("balance", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_accounts_id"), "accounts", ["id"], unique=False)

    if not inspector.has_table("transfer_records"):
        op.create_table(
            "transfer_records",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("from_account_id", sa.Integer(), nullable=False),
            sa.Column("to_account_id", sa.Integer(), nullable=False),
            sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
            sa.ForeignKeyConstraint(["from_account_id"], ["accounts.id"]),
            sa.ForeignKeyConstraint(["to_account_id"], ["accounts.id"]),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(op.f("ix_transfer_records_from_account_id"), "transfer_records", ["from_account_id"], unique=False)
        op.create_index(op.f("ix_transfer_records_to_account_id"), "transfer_records", ["to_account_id"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    if inspector.has_table("transfer_records"):
        op.drop_index(op.f("ix_transfer_records_to_account_id"), table_name="transfer_records")
        op.drop_index(op.f("ix_transfer_records_from_account_id"), table_name="transfer_records")
        op.drop_table("transfer_records")

    if inspector.has_table("accounts"):
        op.drop_index(op.f("ix_accounts_id"), table_name="accounts")
        op.drop_table("accounts")
