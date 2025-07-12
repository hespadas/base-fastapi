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


def test_update_project(client, user, project, token):
    response = client.put(
        f"/api/projects/{project.id}",
        json={
            "title": "Updated Project",
            "description": "This is an updated test project.",
            "github_url": "www.updatedproject.com",
            "project_url": "www.updatedproject.com",
            "user_id": user.id,
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": project.id,
        "title": "Updated Project",
        "description": "This is an updated test project.",
        "github_url": "www.updatedproject.com",
        "project_url": "www.updatedproject.com",
        "user_id": user.id,
    }
