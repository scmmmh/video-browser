"""Models for the videos."""
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, Unicode, UnicodeText, DateTime, func
from sqlalchemy.orm import relationship

from video_browser.models.meta import Base


def utcnow():
    """Return the current UTC datetime without timezone info."""
    return datetime.now(tz=UTC).replace(tzinfo=None)


class Video(Base):
    """Database model for a single video."""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True)
    public_id = Column(Unicode(255), unique=True)
    title = Column(Unicode(255))
    description = Column(UnicodeText())
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, nullable=True, onupdate=utcnow)

    items = relationship("PlaylistItem", back_populates="video")
