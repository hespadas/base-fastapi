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

def test_create_project_without_authentication(client):
    response = client.post(
        "/api/projects",
        json={
            "title": "Test Project",
            "description": "This is a test project.",
            "user_id": 1,
            "github_url": "www.testproject.com",
            "project_url": "www.testproject.com",
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Not authenticated"}


def test_update_project(client, user, project, token):
    response = client.put(
        f"/api/projects/{project.id}",
        json={
            "title": "Updated Project",
            "description": "This is an updated test project.",
            "github_url": "www.updatedproject.com",
            "project_url": "www.updatedproject.com",
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

def test_get_projects(client, user, project, token):
    response = client.get(
        "/api/projects",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "github_url": project.github_url,
        "project_url": project.project_url,
        "user_id": user.id,
    }
