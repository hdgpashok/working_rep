from contextlib import contextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.config import Settings

settings = Settings()

engine = create_async_engine(str(settings.postgres_url))


@contextmanager
async def get_session() -> AsyncSession:
    session: AsyncSession = AsyncSession(engine)
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
