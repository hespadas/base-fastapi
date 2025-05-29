from http import HTTPStatus


def test_create_user(client):
    response = client.post(
        "/users/users",
        json={
            "username": "testusername",
            "email": "testemail@test.com",
            "password": "testpassword",
        }
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "testusername",
        "email": "testemail@test.com",
    }


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "testusername",
                "email": "testemail@test.com",
            }
        ]
    }

def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "updatedusername",
            "email": "newemail@test.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": "updatedusername",
        "email": "newemail@test.com"
        }


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.NO_CONTENT
