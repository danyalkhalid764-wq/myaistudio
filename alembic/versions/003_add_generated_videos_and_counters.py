"""Add generated_videos table and daily counters on users

Revision ID: 003_add_generated_videos_and_counters
Revises: 002_add_generated_images
Create Date: 2025-10-29 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_generated_videos_and_counters'
down_revision = '002_add_generated_images'
branch_labels = None
depends_on = None


def upgrade():
    # Detect database type for datetime defaults
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    # SQLite uses datetime('now'), PostgreSQL uses now()
    datetime_default = sa.text("(datetime('now'))") if is_sqlite else sa.text('now()')
    
    # Users counters and reset date
    op.add_column('users', sa.Column('daily_voice_count', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('daily_video_count', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('last_reset_date', sa.Date(), nullable=True))
    # Standardize default plan name to Free if previously Trial
    # Note: raw SQL is safe enough here
    op.execute("UPDATE users SET plan='Free' WHERE plan IS NULL OR plan='Trial'")

    # Generated videos table
    op.create_table(
        'generated_videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('video_url', sa.String(), nullable=False),
        sa.Column('duration_seconds', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=datetime_default, nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_generated_videos_id'), 'generated_videos', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_generated_videos_id'), table_name='generated_videos')
    op.drop_table('generated_videos')
    op.drop_column('users', 'last_reset_date')
    op.drop_column('users', 'daily_video_count')
    op.drop_column('users', 'daily_voice_count')












