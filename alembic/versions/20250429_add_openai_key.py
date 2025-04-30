"""add openai_api_key to users

Revision ID: 20250430_add_openai_api_key
Revises: 20250429_create_users_table
Create Date: 2025-04-30 09:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = "20250430_add_openai_api_key"
down_revision = "20250429_create_users_table"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        "users",
        sa.Column("openai_api_key", sa.String(length=255), nullable=True),
    )

def downgrade():
    op.drop_column("users", "openai_api_key")
