import uuid

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import Redis

from src.application import get_app
from src.models.base import Base
from src.session import get_session
from src.dependencies.user_service import get_user_service
from src.services.users import UserService
from config.redis_cache import CacheService
from src.schemas.profiles import ProfileCreate
from src.schemas.users import UserCreate


app = get_app()


@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer(
            "postgres:15",
            username="test",
            password="test",
            dbname="test",
    ) as postgres:
        port = postgres.get_exposed_port(5432)
        yield f"postgresql+asyncpg://test:test@localhost:{port}/test"


@pytest.fixture(scope="session")
def redis_url():
    with RedisContainer("redis:7") as redis:
        host = redis.get_container_host_ip()
        port = redis.get_exposed_port(6379)
        yield f"redis://{host}:{port}/0"


@pytest_asyncio.fixture
async def engine(postgres_url):
    engine = create_async_engine(postgres_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@pytest_asyncio.fixture
async def redis_client(redis_url):
    client = Redis.from_url(redis_url, decode_responses=True)
    yield client
    await client.flushdb()
    await client.aclose()


@pytest_asyncio.fixture
async def cache_service(redis_client):
    return CacheService(redis_client=redis_client)


@pytest.fixture
def mock_id():
    return uuid.UUID("12345678-1234-5678-1234-567812345678")


@pytest.fixture
def user_create_data():
    return UserCreate(
        title="developer",
        profile=ProfileCreate(
            title="profile_title",
            bio="bio",
        ),
    )


@pytest.fixture
def user_create_payload():
    return {
        "title": "developer",
        "profile": {
            "title": "profile_title",
            "bio": "bio",
        },
    }


@pytest_asyncio.fixture
async def user_service(cache_service):
    return UserService(cache=cache_service)


@pytest_asyncio.fixture
async def api_client(session, user_service):
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_user_service] = lambda: user_service

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()