"""Database models for connecting playlists to videos."""
from sqlalchemy import Table, Column, ForeignKey, Integer

from video_browser.models.meta import metadata


playlists_videos = Table(
    "playlist_items",
    metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("video_id", Integer, ForeignKey("videos.id"), primary_key=True),
    Column("order", Integer()),
)
