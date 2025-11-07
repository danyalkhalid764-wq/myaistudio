"""Remove daily counters from users

Revision ID: 004_remove_user_counters
Revises: 003_add_generated_videos_and_counters
Create Date: 2025-10-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_remove_user_counters'
down_revision = '003_add_generated_videos_and_counters'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        # Use try/except to be resilient if columns don't exist
        try:
            batch_op.drop_column('daily_voice_count')
        except Exception:
            pass
        try:
            batch_op.drop_column('daily_video_count')
        except Exception:
            pass
        try:
            batch_op.drop_column('last_reset_date')
        except Exception:
            pass


def downgrade() -> None:
    with op.batch_alter_table('users') as batch_op:
        batch_op.add_column(sa.Column('last_reset_date', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('daily_video_count', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('daily_voice_count', sa.Integer(), nullable=True))







