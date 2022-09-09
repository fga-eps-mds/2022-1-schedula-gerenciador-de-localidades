from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_post_city_as_admin(client: TestClient):
    response = client.post(
        "/city", json={"name": "test"},
        headers=ADMIN_HEADER)
    assert response.status_code == 201


def test_post_city_invalid_name_as_admin(client: TestClient):
    response = client.post(
        "/city",
        json={"name": None},
        headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_post_city_as_manager(client: TestClient):
    response = client.post(
        "/city",
        json={"name": "test"},
        headers=MANAGER_HEADER)
    assert response.status_code == 201


def test_post_city_as_basic(client: TestClient):
    response = client.post(
        "/city",
        json={"name": None},
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_post_city_as_public(client: TestClient):
    response = client.post(
        "/city",
        json={"name": None}
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
