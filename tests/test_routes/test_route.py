import pytest


@pytest.mark.asyncio
async def test_route_create_user(api_client, user_create_payload):
    response = await api_client.post(
        "/api/v1/users_profiles/users",
        json=user_create_payload,
    )

    assert response.status_code == 201
    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "developer"
    assert data["profile"]["title"] == "profile_title"
    assert data["profile"]["bio"] == "bio"


@pytest.mark.asyncio
async def test_route_get_user(api_client, user_create_payload):
    create_resp = await api_client.post(
        "/api/v1/users_profiles/users",
        json=user_create_payload,
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    response = await api_client.get(f"/api/v1/users_profiles/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["title"] == "developer"
    assert data["profile"]["bio"] == "bio"


@pytest.mark.asyncio
async def test_route_update_user(api_client, user_create_payload):
    create_resp = await api_client.post(
        "/api/v1/users_profiles/users",
        json=user_create_payload,
    )
    user_id = create_resp.json()["id"]

    update_payload = {
        "title": "updated_title",
        "profile": {
            "title": "updated_profile",
            "bio": "updated_bio",
        },
    }

    response = await api_client.patch(
        f"/api/v1/users_profiles/users/{user_id}",
        json=update_payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updated_title"
    assert data["profile"]["title"] == "updated_profile"
    assert data["profile"]["bio"] == "updated_bio"


@pytest.mark.asyncio
async def test_route_delete_user(api_client, user_create_payload):
    create_resp = await api_client.post(
        "/api/v1/users_profiles/users",
        json=user_create_payload,
    )
    user_id = create_resp.json()["id"]

    response = await api_client.delete(f"/api/v1/users_profiles/users/{user_id}")
    assert response.status_code == 204

    get_resp = await api_client.get(f"/api/v1/users_profiles/users/{user_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_route_create_external_user(api_client, mock_id):
    payload = {
        "id": str(mock_id),
        "title": "external_title",
        "profile": {
            "id": str(mock_id),
            "title": "external_profile",
            "bio": "external_bio",
        },
    }

    response = await api_client.post(
        "/api/v1/users_profiles/external_user",
        json=payload,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(mock_id)
    assert data["title"] == "external_title"
    assert data["profile"]["title"] == "external_profile"