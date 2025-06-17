from http import HTTPStatus
from app.schemas.experience_schema import ExperiencePublicSchema


def test_create_experience(client, user, token):
    response = client.post(
        "/api/experiences",
        json={
            "title": "Test Experience",
            "description": "This is a test experience.",
            "start_date": "2023-10-01T00:00:00",
            "company": "Espadas Company",
            "user_id": user.id,
            "end_date": "2023-12-31",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Test Experience",
        "description": "This is a test experience.",
        "company": "Espadas Company",
        "start_date": response.json()["start_date"],
        "end_date": "2023-12-31",
    }


def test_create_experience_without_authentication(client):
    response = client.post(
        "/api/experiences",
        json={
            "title": "Test Experience",
            "description": "This is a test experience.",
            "start_date": "2023-10-01T00:00:00",
            "company": "Espadas Company",
            "user_id": 1,
            "end_date": "2023-12-31",
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_get_experiences(client, user, experience):
    experience_schema = ExperiencePublicSchema.model_validate(experience)
    response = client.get(f"/api/experiences/{user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"experiences": [experience_schema.model_dump(mode="json")]}


def test_update_experience(client, user, experience, token):
    response = client.put(
        f"/api/experiences/{experience.id}",
        json={
            "title": "Updated Experience",
            "description": "This is an updated test experience.",
            "start_date": "2023-10-01T00:00:00",
            "company": "Updated Company",
            "end_date": "2024-01-01",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": experience.id,
        "title": "Updated Experience",
        "description": "This is an updated test experience.",
        "company": "Updated Company",
        "start_date": response.json()["start_date"],
        "end_date": "2024-01-01",
    }


def test_delete_experience(client, user, experience, token):
    response = client.delete(f"/api/experiences/{experience.id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NO_CONTENT
