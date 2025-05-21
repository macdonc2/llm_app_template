"""Add FastAPI Users boolean flags and switch id to UUID

Revision ID: 20250519_add_fastapi_users_columns
Revises: 20250501_add_tavily_api_key
Create Date: 2025-05-19 18:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision = "20250519_add_fastapi_users_columns"
down_revision = "20250501_add_tavily_api_key"
branch_labels = None
depends_on = None

def upgrade():
    # Enable uuid-ossp extension so uuid_generate_v4() exists:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # Convert id from VARCHAR to native UUID, generating new values:
    op.alter_column(
        "users", "id",
        existing_type=sa.String(length=64),
        type_=pg.UUID(),
        postgresql_using="uuid_generate_v4()",
        existing_nullable=False,
    )

    # Add only the missing FastAPI-Users boolean flags:
    op.add_column(
        "users",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.sql.expression.true(),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            nullable=False,
            server_default=sa.sql.expression.false(),
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.sql.expression.false(),
        ),
    )

def downgrade():
    # Drop the flags in reverse order
    op.drop_column("users", "is_verified")
    op.drop_column("users", "is_superuser")
    op.drop_column("users", "is_active")

    # Convert id back to a 64-char string (you may lose data here if you’d actually converted to real UUIDs)
    op.alter_column(
        "users", "id",
        existing_type=pg.UUID(),
        type_=sa.String(length=64),
        existing_nullable=False,
    )
