from fastapi import Depends
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from doctor.models import async_session, Base
from sqlalchemy import Column, String
from sqlalchemy_utils import EmailType


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
