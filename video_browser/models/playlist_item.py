"""Database models for connecting playlists to videos."""
from sqlalchemy import Column, ForeignKey, Integer

from video_browser.models.base import Base


class PlaylistItem(Base):
    """Database model for a connecting a Playlist to a Video."""

    __tablename__ = "playlist_items"

    playlist_id = Column(Integer, ForeignKey("playlist.id"), primary_key=True)
    video_id = Column(Integer, ForeignKey("videos.id"), primary_key=True)
    order = Column(Integer())
