import pytest


@pytest.mark.asyncio
async def test_route_create_user(mock_client):
    data = {
        "title": "string",
        "profile": {
            "title": "string",
            "bio": "string"
        }
    }

    response = await mock_client.post(
        "/users",
        json=data,
        follow_redirects=True
    )

    assert response.status_code == 201

    response_data = response.json()

    assert response_data["id"] is not None
    assert response_data["title"] == "string"
    assert response_data["profile"]["title"] == "string"
    assert response_data["profile"]["bio"] == "string"


@pytest.mark.asyncio
async def test_route_get_user(mock_client):
    create_data = {
        "title": "string",
        "profile": {
            "title": "string",
            "bio": "string"
        }
    }

    create_response = await mock_client.post(
        "/users",
        json=create_data
    )

    assert create_response.status_code == 201

    created_user = create_response.json()
    user_id = created_user["id"]

    response = await mock_client.get(f"/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["title"] == create_data["title"]
    assert data["profile"]["title"] == create_data["profile"]["title"]
    assert data["profile"]["bio"] == create_data["profile"]["bio"]