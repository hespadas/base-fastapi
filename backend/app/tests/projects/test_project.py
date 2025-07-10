from http import HTTPStatus


def test_create_project(client, user, token):
    response = client.post(
        "/api/projects",
        json={
            "title": "Test Project",
            "description": "This is a test project.",
            "user_id": user.id,
            "github_url": "www.testproject.com",
            "project_url": "www.testproject.com",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "title": "Test Project",
        "description": "This is a test project.",
        "github_url": "www.testproject.com",
        "project_url": "www.testproject.com",
        "user_id": user.id,
    }

