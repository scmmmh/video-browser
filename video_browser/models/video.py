"""Models for the videos."""
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, Unicode, UnicodeText

from video_browser.models.base import Base


class Video(Base):
    """Database model for a single video."""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    public_id = Column(Unicode(255), unique=True)
    title = Column(Unicode(255))
    description = Column(UnicodeText())


class VideoModel(BaseModel):
    """A pydantic model for validating a video."""

    id: int
    public_id: str
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)
