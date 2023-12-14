"""API for the frontend video browser."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from video_browser.models import db_session, Playlist, PlaylistItem, Video
from video_browser.settings import settings

router = APIRouter(prefix="/api")


@router.get("/")
async def get_api_config(dbsession: Annotated[AsyncSession, Depends(db_session)]) -> dict:
    """Get the API configuration."""
    return {"video_base_url": settings.video_base_url}


class PlaylistModel(BaseModel):
    """A pydantic model for validating a playlist."""

    public_id: str = Field(serialization_alias="id")
    title: str
    description: str
    videos: list[str] = Field(validation_alias="items")

    model_config = ConfigDict(from_attributes=True)

    @field_validator("videos", mode="before")
    @classmethod
    def convert_videos_to_ids(cls, value: list[Video]) -> list[str]:
        """Convert the Video objects to a list of ids."""
        return [item.video.public_id for item in value]


@router.get("/playlists/{pid}", response_model=PlaylistModel)
async def get_playlist(pid: str, dbsession: Annotated[AsyncSession, Depends(db_session)]) -> Playlist:
    """Return a single playlist."""
    query = (
        select(Playlist)
        .filter(Playlist.public_id == pid)
        .options(selectinload(Playlist.items).selectinload(PlaylistItem.video))
    )
    playlist = (await dbsession.execute(query)).scalar()
    if playlist:
        return playlist
    else:
        raise HTTPException(404)


class VideoModel(BaseModel):
    """A pydantic model for validating a video."""

    public_id: str = Field(serialization_alias="id")
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


@router.get("/playlists/{pid}/videos", response_model=list[VideoModel])
async def get_videos(
    pid: str,
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> list[Video]:
    """Get all videos for a playlist."""
    query = select(Video).join(Video.items).join(PlaylistItem.playlist).filter(Playlist.public_id == pid)
    return (await dbsession.execute(query)).scalars()
