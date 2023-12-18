"""API for the frontend video browser."""
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ConfigDict
from shutil import copyfileobj
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import uuid4

from video_browser.backend.api.auth import get_current_user
from video_browser.models import db_session, User, Video
from video_browser.settings import settings


router = APIRouter(prefix="/videos")


class VideoModel(BaseModel):
    """Pydantic model for validating videos."""

    id: int
    public_id: str
    title: str
    description: str

    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[VideoModel])
async def get_all_videos(
    current_user: Annotated[User, Depends(get_current_user)], dbsession: Annotated[AsyncSession, Depends(db_session)]
) -> list[Video]:
    """Fetch all videos."""
    query = select(Video).order_by(desc(Video.created_at))
    return (await dbsession.execute(query)).scalars()


@router.post("/", response_model=VideoModel)
async def create_video(
    title: Annotated[str, Body()],
    description: Annotated[str, Body()],
    video: UploadFile,
    poster: UploadFile,
    transcript: UploadFile,
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> Video:
    """Create a new video."""
    db_video = Video(public_id=str(uuid4()), title=title, description=description)
    with open(os.path.join(settings.data_base_path, f"{db_video.public_id}.mp4"), "wb") as out_f:
        copyfileobj(video.file, out_f)
    with open(os.path.join(settings.data_base_path, f"{db_video.public_id}.png"), "wb") as out_f:
        copyfileobj(poster.file, out_f)
    with open(os.path.join(settings.data_base_path, f"{db_video.public_id}.vtt"), "wb") as out_f:
        copyfileobj(transcript.file, out_f)
    dbsession.add(db_video)
    await dbsession.commit()
    return db_video


@router.get("/{vid}", response_model=VideoModel)
async def get_video(
    vid: int,
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> Video:
    """Retrieve a single video."""
    query = select(Video).filter(Video.id == vid)
    video = (await dbsession.execute(query)).scalar()
    if video is not None:
        return video
    else:
        raise HTTPException(404)


@router.patch("/{vid}", response_model=VideoModel)
async def patch_video(
    vid: int,
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
    title: Annotated[str | None, Body()] = None,
    description: Annotated[str | None, Body()] = None,
    video: UploadFile = None,
    poster: UploadFile = None,
    transcript: UploadFile = None,
) -> Video:
    """Patch the properties of a single video."""
    query = select(Video).filter(Video.id == vid)
    db_video = (await dbsession.execute(query)).scalar()
    if db_video is not None:
        if title is not None:
            db_video.title = title
        if description is not None:
            db_video.description = description
        if video is not None:
            with open(os.path.join(settings.data_base_path, f"{db_video.public_id}.mp4"), "wb") as out_f:
                copyfileobj(video.file, out_f)
        if poster is not None:
            with open(os.path.join(settings.data_base_path, f"{db_video.public_id}.png"), "wb") as out_f:
                copyfileobj(poster.file, out_f)
        if transcript is not None:
            with open(os.path.join(settings.data_base_path, f"{db_video.public_id}.vtt"), "wb") as out_f:
                copyfileobj(transcript.file, out_f)
        await dbsession.commit()
        return db_video
    else:
        raise HTTPException(404)


@router.get("/{vid}/transcript")
async def get_video_transcript(
    vid: int,
    current_user: Annotated[User, Depends(get_current_user)],
    dbsession: Annotated[AsyncSession, Depends(db_session)],
) -> dict:
    """Retrieve the transcript for a single video."""
    query = select(Video).filter(Video.id == vid)
    video = (await dbsession.execute(query)).scalar()
    if video is not None:
        if os.path.exists(os.path.join(settings.data_base_path, f"{video.public_id}.vtt")):
            with open(os.path.join(settings.data_base_path, f"{video.public_id}.vtt")) as in_f:
                return {"text": in_f.read()}
    raise HTTPException(404)
