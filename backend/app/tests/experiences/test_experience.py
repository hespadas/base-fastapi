from http import HTTPStatus
from app.schemas.experience_schema import ExperiencePublicSchema


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


def test_create_experience_without_authentication(client):
    response = client.post(
        "/experiences",
        json={
            "title": "Test Experience",
            "description": "This is a test experience.",
            "start_date": "2023-10-01T00:00:00",
            "company": None,
            "user_id": 1,
            "end_date": None,
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_get_experiences(client, user, experience):
    experience_schema = ExperiencePublicSchema.model_validate(experience)
    response = client.get(f"/experiences/{user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"experiences": [experience_schema.model_dump(mode="json")]}


