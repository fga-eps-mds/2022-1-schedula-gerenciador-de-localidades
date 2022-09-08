from fastapi.testclient import TestClient
from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER

def test_get_city_as_admin(client:TestClient):
    url = "/city"
    response = client.get(url,headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9

def test_get_city_id_as_admin(client:TestClient):
    url = "/city?city_id=2"
    response = client.get(url,headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["data"] == {"id": 2, "name": "Cidade 2"}


def test_city_id_not_found_admin(client:TestClient):
    response = client.get("/city?city_id=12",headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["message"] == "Nenhuma cidade encontrada"

## get city as manager


def test_get_city_as_manager(client: TestClient):
    response = client.get("/city", headers=MANAGER_HEADER)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9

# get city as basic

def test_get_city_as_basic(client: TestClient):
    response = client.get("/city", headers=BASIC_HEADER)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9

#get city as public

def test_get_city_as_public(client: TestClient):
    response = client.get("/city")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 9

