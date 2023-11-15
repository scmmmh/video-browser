"""Add playlists table.

Revision ID: 6000f4309678
Revises: b6060bb44990
Create Date: 2023-11-15 17:14:40.565981

"""
from alembic import op
from sqlalchemy import Column, Integer, Unicode, UnicodeText

from video_browser.models.meta import metadata


# revision identifiers, used by Alembic.
revision = '6000f4309678'
down_revision = 'b6060bb44990'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the new playlists table."""
    op.create_table(
        "playlists",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("public_id", Unicode(255)),
        Column("title", Unicode(255)),
        Column('description', UnicodeText()),
    )


def downgrade() -> None:
    """Drop the playlists table."""
    op.drop_table("playlists")
