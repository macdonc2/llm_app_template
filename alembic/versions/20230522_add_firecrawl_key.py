"""Add firecrawl_api_key to users

Revision ID: 20250522_add_firecrawl_api_key
Revises: 361ff68b3b4f
Create Date: 2025-05-22 18:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20250522_add_firecrawl_api_key"
down_revision = "361ff68b3b4f"
branch_labels = None
depends_on = None


def upgrade():
    # Add the new API key column (nullable so existing rows continue to work)
    op.add_column(
        "users",
        sa.Column(
            "firecrawl_api_key",
            sa.String(length=512),
            nullable=True,
        ),
    )


def downgrade():
    # Simply drop the column on downgrade
    op.drop_column("users", "firecrawl_api_key")
