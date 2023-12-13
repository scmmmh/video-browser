"""Add users table.

Revision ID: 494808ee9b5a
Revises: 359ee7173888
Create Date: 2023-12-13 15:13:24.694496

"""
from alembic import op
from sqlalchemy import Column, Integer, Unicode, UnicodeText

from video_browser.models.meta import metadata


# revision identifiers, used by Alembic.
revision = '494808ee9b5a'
down_revision = '359ee7173888'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create the new users table."""
    op.create_table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("email", Unicode(255)),
        Column("password", Unicode(255)),
        Column("name", Unicode(255)),
    )
    op.create_index(None, "users", ["email"])


def downgrade() -> None:
    """Drop the users table."""
    op.drop_index("ix_users_email")
    op.drop_table("users")
