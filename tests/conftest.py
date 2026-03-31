import uuid
import pytest
import pytest_asyncio

from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.schemas.profiles import ProfileCreate
from src.schemas.users import UserCreate
from src.models.base import Base


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
        id=uuid.UUID("12345678-1234-5678-1234-567812345678"),
        title="test",
        profile=mock_create_profile
    )


