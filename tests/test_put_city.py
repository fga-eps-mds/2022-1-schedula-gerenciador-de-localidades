from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_put_city_as_admin(client: TestClient):
    response = client.put(
        "/city/1",
        json={
            "name": "new test"},
        headers=ADMIN_HEADER)
    assert response.status_code == 200


def test_put_city_invalid_name_as_admin(client: TestClient):
    response = client.put("/city/1", json={"name": None}, headers=ADMIN_HEADER)
    assert response.status_code == 422


def test_put_invalid_city_as_admin(client: TestClient):
    response = client.put(
        "/city/12",
        json={
            "name": "test"},
        headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Cidade não encontrada"


def test_put_city_as_manager(client: TestClient):
    response = client.put(
        "/city/1",
        json={
            "name": "new test"},
        headers=MANAGER_HEADER)
    assert response.status_code == 200


def test_put_category_as_basic(client: TestClient):
    response = client.put(
        "/city/1",
        json={"name": "new test"},
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_put_category_as_public(client: TestClient):
    response = client.put(
        "/city/1",
        json={"name": "new test"}
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
