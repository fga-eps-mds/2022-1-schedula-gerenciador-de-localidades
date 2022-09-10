from urllib import response

from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_get_workstation_as_admin(client: TestClient):
    url = "/workstation"
    response = client.get(
        url, headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "dados buscados com sucesso"
    assert len(response.json()["data"]) == 4


def test_get_workstation_by_regional(client: TestClient):
    url = "/workstation?regional=True"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["message"] == "dados buscados com sucesso"
    assert len(response.json()["data"]) == 2


def test_get_workstation_id_as_admin(client: TestClient):
    url = "/workstation?id=1"
    response = client.get(url, headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["data"] == {
        "id": 1,
        "city_id": 1,
        "name": "1ª DP de Goiânia",
        "ip": "127.0.0.0",
        "link": "exemplo de link",
        "adsl_vpn": True,
        "regional": True,
        "regional_id": None,
        "active": False,
        "phones": [],
    }


def test_workstation_id_not_found_as_admin(client: TestClient):
    response = client.get("/workstation?id=12", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "dados não encontrados"

# get as manager


def test_get_workstation_as_manager(client: TestClient):
    url = "/workstation"
    response = client.get(
        url, headers=MANAGER_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "dados buscados com sucesso"
    assert len(response.json()["data"]) == 4

# get as basic


def test_get_workstation_as_basic(client: TestClient):
    url = "/workstation"
    response = client.get(
        url, headers=BASIC_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "dados buscados com sucesso"
    assert len(response.json()["data"]) == 4

# get as public


def test_get_workstation_as_public(client: TestClient):
    url = "/workstation"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["message"] == "dados buscados com sucesso"
    assert len(response.json()["data"]) == 4
