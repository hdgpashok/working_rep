import uuid
from unittest.mock import patch
from uuid import UUID

import pytest

from src.repository.user import UserRepository


@pytest.mark.asyncio
async def test_create_user_service(mock_id, mock_create_user, mock_session):

    with patch("src.repository.user.uuid.uuid4", return_value=mock_id):
        res = await UserRepository.create_user_db(mock_create_user, mock_session)

    assert res.id is not None
    assert res.title == "test"

    assert res.profile.id is not None
    assert res.profile.title == 'test'


@pytest.mark.asyncio
async def test_get_user_service(mock_id, mock_session):
    res = await UserRepository.select(mock_id, mock_session)

    assert res.id == mock_id
    assert res.title == "test"

    assert res.profile.id is not None
    assert res.profile.title == 'test'
    assert res.profile.bio == "test_bio"

