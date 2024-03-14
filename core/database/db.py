from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncAttrs
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=True)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass
