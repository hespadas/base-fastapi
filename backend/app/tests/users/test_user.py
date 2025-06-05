from http import HTTPStatus
from app.schemas.user_schema import UserPublicSchema


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "testusername",
            "email": "testemail@test.com",
            "password": "testpassword",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "testusername",
        "email": "testemail@test.com",
    }


def test_get_users(client, user):
    user_schema = UserPublicSchema.model_validate(user)
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema.model_dump(mode="json")]}


def test_update_user(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        json={"username": "updatedusername", "email": "newemail@test.com", "password": "newpassword"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": user.id, "username": "updatedusername", "email": "newemail@test.com"}


def test_update_user_with_wrong_user(client, another_user, token):
    response = client.put(
        f"/users/{another_user.id}",
        json={"username": "updatedusername", "email": "email@example.com", "password": "mynewpassword"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not allowed to update this user."}


def test_delete_user(client, user, token):
    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT
