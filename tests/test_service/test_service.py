import pytest
from src.exceptions.not_found import ObjectNotFound
from src.schemas.users import UserUpdate
from src.schemas.profiles import ProfileUpdate


@pytest.mark.asyncio
async def test_create_user_service(user_service, user_create_data, session):
    result = await user_service.create_user_db(user_create_data, session)

    assert result.id is not None
    assert result.title == "developer"
    assert result.profile.id is not None
    assert result.profile.title == "profile_title"
    assert result.profile.bio == "bio"


@pytest.mark.asyncio
async def test_get_user_service(user_service, user_create_data, session):
    created = await user_service.create_user_db(user_create_data, session)
    await session.commit()

    result = await user_service.get_users_with_profile(created.id, session)

    assert result.id == created.id
    assert result.title == "developer"
    assert result.profile.title == "profile_title"
    assert result.profile.bio == "bio"


@pytest.mark.asyncio
async def test_update_user_service(user_service, user_create_data, session):

    created = await user_service.create_user_db(user_create_data, session)
    await session.commit()

    update_data = UserUpdate(
        title="updated_title",
        profile=ProfileUpdate(title="updated_profile", bio="updated_bio"),
    )

    result = await user_service.update_user_db(created.id, update_data, session)

    assert result.id == created.id
    assert result.title == "updated_title"
    assert result.profile.title == "updated_profile"
    assert result.profile.bio == "updated_bio"


@pytest.mark.asyncio
async def test_delete_user_service(user_service, user_create_data, session):
    created = await user_service.create_user_db(user_create_data, session)
    await session.commit()

    await user_service.delete_user_db(created.id, session)
    await session.commit()

    with pytest.raises(ObjectNotFound):
        await user_service.get_users_with_profile(created.id, session)