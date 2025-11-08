"""add missing user columns

Revision ID: 006_add_missing_user_columns
Revises: 005_add_total_tokens_used
Create Date: 2025-11-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006_add_missing_user_columns'
down_revision = '005_add_total_tokens_used'
branch_labels = None
depends_on = None


def upgrade():
    # Add missing columns to users table if they don't exist
    # Check if columns exist before adding (SQLite doesn't support IF NOT EXISTS)
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    # Add daily_voice_count if it doesn't exist
    if 'daily_voice_count' not in columns:
        op.add_column('users', sa.Column('daily_voice_count', sa.Integer(), nullable=True, server_default='0'))
    
    # Add last_reset_date if it doesn't exist
    if 'last_reset_date' not in columns:
        op.add_column('users', sa.Column('last_reset_date', sa.Date(), nullable=True))


def downgrade():
    # Remove columns if they exist
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    columns = [col['name'] for col in inspector.get_columns('users')]
    
    if 'last_reset_date' in columns:
        op.drop_column('users', 'last_reset_date')
    
    if 'daily_voice_count' in columns:
        op.drop_column('users', 'daily_voice_count')

