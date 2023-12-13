"""Models for the users."""
from sqlalchemy import Column, Integer, Unicode, Index

from video_browser.models.meta import Base


class User(Base):
    """Database model for a user."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(Unicode(255))
    password = Column(Unicode(255))
    name = Column(Unicode(255))


Index(User.email)
