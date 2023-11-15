"""Database models for playlists."""
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, Unicode, UnicodeText

from video_browser.models.base import Base


class Playlist(Base):
    """Database model for a single playlist."""

    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    public_id = Column(Unicode(255), unique=True)
    title = Column(Unicode(255))
    description = Column(UnicodeText())


class PlaylistModel(BaseModel):
    """A pydantic model for validating a playlist."""

    id: int
    public_id: str
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)
