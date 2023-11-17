"""Models for the videos."""
from sqlalchemy import Column, Integer, Unicode, UnicodeText
from sqlalchemy.orm import relationship

from video_browser.models.meta import Base
from video_browser.models.playlist_item import playlists_videos


class Video(Base):
    """Database model for a single video."""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    public_id = Column(Unicode(255), unique=True)
    title = Column(Unicode(255))
    description = Column(UnicodeText())

    playlists = relationship("Playlist", secondary=playlists_videos, order_by="Playlist.title", back_populates="videos")
