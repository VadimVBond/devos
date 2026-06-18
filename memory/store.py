import uuid
from datetime import datetime
from typing import Any
from sqlalchemy import String, Text, JSON, DateTime, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker
from loguru import logger

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(1024))
    stack: Mapped[str | None] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(50), default="active")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    intent: Mapped[str] = mapped_column(Text)
    action: Mapped[str] = mapped_column(String(255))
    input_data: Mapped[dict | None] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    risk_level: Mapped[str] = mapped_column(String(20), default="low")
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# Database Setup
DATABASE_URL = "sqlite+aiosqlite:///memory/sqlite.db"
engine = create_async_engine(DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.success("Database initialized.")

async def create_session(session_name: str):
    logger.info(f"Memory: Creating session '{session_name}'")
    return True

async def store_kv(key: str, value: Any):
    logger.info(f"Memory: Storing {key} = {value}")
    return True
