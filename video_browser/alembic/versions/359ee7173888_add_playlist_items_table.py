"""Add playlist_items table.

Revision ID: 359ee7173888
Revises: 6000f4309678
Create Date: 2023-11-15 17:14:45.915601

"""
from alembic import op
from sqlalchemy import Column, ForeignKey, Integer

from video_browser.models.meta import metadata


# revision identifiers, used by Alembic.
revision = '359ee7173888'
down_revision = '6000f4309678'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the new playlist_items table."""
    op.create_table(
        "playlist_items",
        metadata,
        Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
        Column("video_id", Integer, ForeignKey("videos.id"), primary_key=True),
        Column("order", Integer),
    )


def downgrade() -> None:
    """Drop the playlist_items table."""
    op.drop_table("playlist_items")
