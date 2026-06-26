import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock

from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.services.users import UserService
from redis_cache import CacheService
from src.core.dependencies import get_session, get_user_service
from src.application import get_app
from src.schemas.profiles import ProfileCreate
from src.schemas.users import UserCreate
from src.models.base import Base


app = get_app()


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15", username="test", password="test", dbname="test") as postgres:
        port = postgres.get_exposed_port(5432)
        yield f"postgresql+asyncpg://test:test@localhost:{port}/test"


@pytest_asyncio.fixture
async def mock_async_engine(postgres_container):
    engine = create_async_engine(postgres_container)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def mock_session(mock_async_engine):
    async_session_maker = async_sessionmaker(mock_async_engine, expire_on_commit=False)

    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture
def mock_id():
    return uuid.UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def mock_create_profile():
    return ProfileCreate(
        nickname="test",
        title="test",
        bio="test",
    )


@pytest.fixture
def mock_create_user(mock_create_profile):
    return UserCreate(
        first_name="test",
        last_name="test",
        title="test",
        profile=mock_create_profile
    )


@pytest_asyncio.fixture
async def mock_user_service(mock_create_user):
    service = AsyncMock()
    service.create_user_db = AsyncMock()
    service.get_users_with_profile = AsyncMock(return_value=mock_create_user)
    service.update_user_db = AsyncMock()
    service.delete_user_db = AsyncMock()
    service.create_external_user = AsyncMock()
    return service


@pytest_asyncio.fixture
async def mock_cache():
    cache = AsyncMock(spec=CacheService)
    cache.get = AsyncMock(return_value=None)
    cache.set = AsyncMock(return_value=True)
    cache.delete = AsyncMock(return_value=True)
    return cache


@pytest_asyncio.fixture
async def mock_client(mock_session, mock_cache):
    app.dependency_overrides[get_session] = lambda: mock_session
    app.dependency_overrides[get_user_service] = lambda: UserService(cache=mock_cache)

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1/users_profiles",
    ) as cli:
        yield cli

    app.dependency_overrides.clear()


