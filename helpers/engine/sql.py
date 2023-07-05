from asyncio import current_task

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import settings
from settings.base import build_sqlalchemy_database_uri

mysql_engine = create_async_engine(
    url=build_sqlalchemy_database_uri(),
    future=True,
    echo=True,
    pool_pre_ping=True,
)


def get_sql_session():
    async_session_factory = sessionmaker(
        mysql_engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_scoped_session(
        async_session_factory, scopefunc=current_task
    )
