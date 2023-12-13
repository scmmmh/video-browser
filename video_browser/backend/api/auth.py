"""API for the frontend video browser."""
import jwt

from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import PlainTextResponse
from passlib.hash import argon2
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from video_browser.models import db_session, User


router = APIRouter(prefix="/auth")


class LoginModel(BaseModel):
    """A pydantic model for validating logging in."""

    email: EmailStr
    password: str


@router.post("/login", response_class=PlainTextResponse)
async def login(authData: LoginModel, dbsession: Annotated[AsyncSession, Depends(db_session)]) -> str:
    """Log the user into the application."""
    query = select(User).filter(User.email == authData.email)
    user = (await dbsession.execute(query)).scalar()
    if user is not None:
        if argon2.verify(authData.password, user.password):
            return jwt.encode(
                {
                    "iss": "video_browser",
                    "exp": datetime.now(tz=UTC) + timedelta(days=1),
                    "iat": datetime.now(tz=UTC),
                    "nbf": datetime.now(tz=UTC),
                    "sub": user.id,
                },
                "secret",
                algorithm="HS256",
            )
    raise HTTPException(403)


async def get_current_user(
    authorization: Annotated[str, Header()], dbsession: Annotated[AsyncSession, Depends(db_session)]
) -> User:
    """Get the current authenticated user based on the Authorization header value."""
    if authorization.startswith("Bearer "):
        token = jwt.decode(
            authorization[7:],
            "secret",
            issuer="video_browser",
            algorithms=["HS256"],
            options={"require": ["iss", "exp", "iat", "nbf", "sub"]},
        )
        query = select(User).filter(User.id == token["sub"])
        user = (await dbsession.execute(query)).scalar()
        if user is not None:
            return user
    raise HTTPException(403)


class UserModel(BaseModel):
    """A pydantic model for validating a single user."""

    id: int
    email: str
    name: str


@router.get("/user", response_model=UserModel)
async def user(user: Annotated[User, Depends(get_current_user)]) -> User:
    """Get the logged-in user."""
    return user
