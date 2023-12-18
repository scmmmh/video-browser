"""Add video created/update at timestamps.

Revision ID: 873dcd4cc027
Revises: 494808ee9b5a
Create Date: 2023-12-18 19:15:58.623004

"""
from alembic import op
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, DateTime, Table, MetaData, select, update

from video_browser.models.meta import metadata


# revision identifiers, used by Alembic.
revision = '873dcd4cc027'
down_revision = '494808ee9b5a'
branch_labels = None
depends_on = None

videos = Table(
    "videos",
    MetaData(),
    Column("id", Integer, primary_key=True),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
)


def upgrade() -> None:
    """Add the created_at and updated_at columns with current data."""
    op.add_column("videos", Column("created_at", DateTime()))
    op.add_column("videos", Column("updated_at", DateTime(), nullable=True))

    for video in op.get_bind().execute(select(videos)).scalars():
        op.execute(
            update(videos)
            .where(videos.c.id == video)
            .values(created_at=datetime.now(tz=UTC).replace(tzinfo=None), updated_at=None)
        )


def downgrade() -> None:
    """Remove the updated_at and created_at columns."""
    op.drop_column("videos", "updated_at")
    op.drop_column("videos", "created_at")
