import uuid
from unittest.mock import patch, AsyncMock

import pytest

from src.services.users import UserService   # ← главный импорт


@pytest.mark.asyncio
async def test_create_user_service(mock_id, mock_create_user, mock_session, mock_cache):
    user_service = UserService(cache=mock_cache)

    # Правильный патч uuid4 — патчим там, где он реально импортируется
    with patch("uuid.uuid4", return_value=mock_id):
        res = await user_service.create_user_db(mock_create_user, mock_session)

    assert res.id is not None
    assert res.title == "test"

    assert res.profile.id is not None
    assert res.profile.title == 'test'


@pytest.mark.asyncio
async def test_get_user_service(mock_id, mock_session, mock_cache):
    user_service = UserService(cache=mock_cache)

    # Мокаем репозиторий
    with patch("src.repository.user.UserRepository.select") as mock_select:
        mock_select.return_value = {
            "id": mock_id,
            "title": "test",
            "profile": {
                "id": mock_id,
                "title": "test",
                "bio": "test_bio"
            }
        }

        res = await user_service.get_users_with_profile(mock_id, mock_session)

    assert res.id == mock_id
    assert res.title == "test"
    assert res.profile.id is not None
    assert res.profile.title == 'test'
    assert res.profile.bio == "test_bio"


@pytest.mark.asyncio
async def test_get_user_service(mock_id, mock_session, mock_cache):
    # Создаём UserService с мок-кэшем
    user_service = UserService(cache=mock_cache)

    # Мокаем получение из репозитория
    with patch("src.repository.user.UserRepository.select") as mock_select:
        mock_select.return_value = {
            "id": mock_id,
            "title": "test",
            "profile": {
                "id": mock_id,
                "title": "test",
                "bio": "test_bio"
            }
        }

        res = await user_service.get_users_with_profile(mock_id, mock_session)

    assert res.id == mock_id
    assert res.title == "test"

    assert res.profile.id is not None
    assert res.profile.title == 'test'
    assert res.profile.bio == "test_bio"