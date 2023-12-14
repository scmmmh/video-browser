"""Database models for connecting playlists to videos."""
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from video_browser.models.meta import Base


class PlaylistItem(Base):
    """Database model for a single playlist item."""

    __tablename__ = "playlist_items"

    playlist_id = Column(Integer, ForeignKey("playlists.id"), primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), primary_key=True)
    order = Column(Integer)

    playlist = relationship("Playlist", back_populates="items")
    video = relationship("Video", back_populates="items")
