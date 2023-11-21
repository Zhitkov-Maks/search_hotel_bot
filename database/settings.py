from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

BASE_DIR = Path(__file__).parent.parent

DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/hotel-db.sqlite3"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Function to get a session."""
    async with async_session_maker() as session:
        yield session
