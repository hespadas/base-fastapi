from http import HTTPStatus


def test_create_experience(client, user, token):
    response = client.post(
        "/experiences",
        json={
            "title": "Test Experience",
            "description": "This is a test experience.",
            "start_date": "2023-10-01T00:00:00",
            "company": None,
            "user_id": user.id,
            "end_date": None,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Test Experience",
        "description": "This is a test experience.",
        "company": None,
        "start_date": response.json()["start_date"],
        "end_date": None,
    }
