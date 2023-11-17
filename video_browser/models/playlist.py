"""Database models for playlists."""
from sqlalchemy import Column, Integer, Unicode, UnicodeText
from sqlalchemy.orm import relationship

from video_browser.models.meta import Base
from video_browser.models.playlist_item import playlists_videos


class Playlist(Base):
    """Database model for a single playlist."""

    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    public_id = Column(Unicode(255), unique=True)
    title = Column(Unicode(255))
    description = Column(UnicodeText())

    videos = relationship(
        "Video", secondary=playlists_videos, order_by=playlists_videos.c.order, back_populates="playlists"
    )
