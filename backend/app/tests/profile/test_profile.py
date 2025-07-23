from http import HTTPStatus


def test_get_data_from_profile(client, user, experience, project):
    response = client.get(
        f"/api/profile/{user.id}",
    )
    assert response.status_code == HTTPStatus.OK
    return response.json()
