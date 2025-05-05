"""Add tavily_api_key to users

Revision ID: 20250501_add_tavily_api_key
Revises: 20250430_add_openai_api_key
Create Date: 2025-05-02 10:00:00.000000
 """

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20250501_add_tavily_api_key'
down_revision = '20250430_add_openai_api_key'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'users',
        sa.Column('tavily_api_key', sa.String(), nullable=True),
    )

def downgrade():
    op.drop_column('users', 'tavily_api_key')
