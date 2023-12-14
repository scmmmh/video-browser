"""API for the frontend video browser."""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict, field_validator, model_validator, Field
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import Annotated

from video_browser.backend.api.auth import get_current_user
from video_browser.backend.api.videos import VideoModel
from video_browser.models import db_session, User, Playlist, PlaylistItem, Video


router = APIRouter(prefix="/playlists")


class PlaylistModel(BaseModel):
    """Pydantic model for validating videos."""

    id: int
    public_id: str
    title: str
    videos: list[int] = Field(validation_alias="items")
    thumbnail: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("videos", mode="before")
    @classmethod
    def convert_video_ids(cls: "PlaylistModel", value: list[Video]) -> list[int]:
        """Convert the list of PlaylistItems to video ids."""
        return [obj.video_id for obj in value]

    @model_validator(mode="before")
    @classmethod
    def determine_thumbnail(cls: "PlaylistModel", playlist: Playlist) -> Playlist:
        """Set a thumbnail if there are video items."""
        if len(playlist.items) > 0:
            setattr(playlist, "thumbnail", playlist.items[0].video.public_id)
        return playlist


@router.get("/", response_model=list[PlaylistModel])
async def get_all_playlists(
    current_user: Annotated[User, Depends(get_current_user)], dbsession: Annotated[AsyncSession, Depends(db_session)]
) -> list[PlaylistModel]:
    """Fetch all playlists."""
    query = select(Playlist).options(selectinload(Playlist.items).selectinload(PlaylistItem.video))
    return (await dbsession.execute(query)).scalars()


@router.get("/{pid}", response_model=PlaylistModel)
async def get_playlist(
    pid: int,
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> Playlist:
    """Retrieve a single playlist."""
    query = (
        select(Playlist)
        .filter(Playlist.id == pid)
        .options(selectinload(Playlist.items).selectinload(PlaylistItem.video))
    )
    playlist = (await dbsession.execute(query)).scalar()
    if playlist is not None:
        return playlist
    else:
        raise HTTPException(404)


@router.get("/{pid}/videos", response_model=list[VideoModel])
async def get_playlist_videos(
    pid: int,
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> list[Video]:
    """Retrieve the videos for a single playlist."""
    query = select(Playlist).filter(Playlist.id == pid)
    playlist = (await dbsession.execute(query)).scalar()
    if playlist is not None:
        query = (
            select(Video)
            .join(Video.items)
            .join(PlaylistItem.playlist)
            .filter(Playlist.id == pid)
            .order_by(PlaylistItem.order)
        )
        return (await dbsession.execute(query)).scalars()
    else:
        raise HTTPException(404)


@router.put("/{pid}/videos", response_model=list[VideoModel])
async def update_playlist_videos(
    pid: int,
    videos: list[VideoModel],
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> list[Video]:
    """Update the videos of a single playlist."""
    query = select(Playlist).filter(Playlist.id == pid)
    playlist = (await dbsession.execute(query)).scalar()
    if playlist is not None:
        delete_query = delete(PlaylistItem).filter(PlaylistItem.playlist_id == pid)
        await dbsession.execute(delete_query)
        await dbsession.commit()
        for idx, video in enumerate(videos):
            dbsession.add(PlaylistItem(playlist_id=pid, video_id=video.id, order=idx))
        await dbsession.commit()
        return await get_playlist_videos(pid, current_user=current_user, dbsession=dbsession)
    else:
        raise HTTPException(404)
