from sqlalchemy import JSON, Column
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, Field
from typing import Any

from app.config import config

DATABASE_URL = config.get("database.url")
if not DATABASE_URL:
    raise ValueError("Missing required configuration: database.url")

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    connect_args={
        "prepared_statement_cache_size": 0,
        "statement_cache_size": 0,
    }
)

SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# TODO: refactor models into seperate structure!
# NOTE: need to discuss strucutre before that

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    hackclub_oauth_response: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )
    hackatime_oauth_response: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )
    hackclub_authorization: str | None = Field(default=None)
    hackatime_authorization: str | None = Field(default=None)
    identity: dict[str, Any] | None = Field(
        default=None,
        sa_column=Column(JSON, nullable=True),
    )