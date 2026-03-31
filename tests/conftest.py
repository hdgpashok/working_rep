import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastapi.testclient import TestClient

from src.db import get_session
from src.application import get_app
from src.schemas.profiles import ProfileCreate
from src.schemas.users import UserCreate, UserOut
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
def mock_create_profile(mock_id):
    return ProfileCreate(
        id=mock_id,
        title='test',
        bio='test_bio'
    )


@pytest.fixture
def mock_create_user(mock_id, mock_create_profile):
    return UserCreate(
        id=mock_id,
        title="test",
        profile=mock_create_profile
    )


@pytest_asyncio.fixture
async def mock_client(mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test/api/v1/users_profiles",
    ) as cli:
        yield cli

    app.dependency_overrides.clear()


@pytest.fixture
def mock_user_service():
    class MockService:
        async def create_user_db(self, data: UserCreate):
            return UserOut(
                id=mock_id(),
                title=data.title,
                profile=data.profile
            )

        async def get_users_with_profile(self, user_id: uuid.UUID):
            return UserOut(
                id=user_id,
                title="test",
                profile=mock_create_profile()
            )

    return MockService()