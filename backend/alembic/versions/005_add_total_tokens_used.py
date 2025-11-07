"""add total_tokens_used

Revision ID: 005
Revises: 004
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_add_total_tokens_used'
down_revision = '004_remove_user_counters'
branch_labels = None
depends_on = None


def upgrade():
    # Add total_tokens_used column to users table
    op.add_column('users', sa.Column('total_tokens_used', sa.Integer(), nullable=True, server_default='0'))


def downgrade():
    # Remove total_tokens_used column
    op.drop_column('users', 'total_tokens_used')

