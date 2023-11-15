"""Add videos table.

Revision ID: b6060bb44990
Revises:
Create Date: 2023-11-15 15:18:52.721067
"""
from alembic import op
from sqlalchemy import Column, Integer, Unicode, UnicodeText

from video_browser.models.meta import metadata


# revision identifiers, used by Alembic.
revision = 'b6060bb44990'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the new videos table."""
    op.create_table(
        "videos",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("public_id", Unicode(255)),
        Column("title", Unicode(255)),
        Column('description', UnicodeText()),
    )


def downgrade() -> None:
    """Drop the videos table."""
    op.drop_table("videos")
