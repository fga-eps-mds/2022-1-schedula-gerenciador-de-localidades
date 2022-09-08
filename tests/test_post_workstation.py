from fastapi.testclient import TestClient
from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER

def test_post_workstation_as_admin(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999", "(61) 99989-9999"],
        },
        headers=ADMIN_HEADER
    )
    assert response.status_code == 201


def test_post_city_error_as_admin(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": True,
            "city_id": 50,
        },
        headers=ADMIN_HEADER
    )
    assert response.status_code == 400


def test_post_regional_error_as_admin(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": False,
            "city_id": 5,
        },
        headers=ADMIN_HEADER
    )
    assert response.status_code == 400

##post as manager

def test_post_workstation_as_manager(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999", "(61) 99989-9999"],
        },
        headers=MANAGER_HEADER
    )
    assert response.status_code == 201


def test_post_city_error_as_manager(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": True,
            "city_id": 50,
        },
        headers=MANAGER_HEADER
    )
    assert response.status_code == 400

def test_post_regional_error_as_manager(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": False,
            "city_id": 5,
        },
        headers=MANAGER_HEADER
    )
    assert response.status_code == 400

## post as basic

def test_post_workstation_as_basic(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": False,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": False,
            "city_id": 1,
            "phones": ["(61) 99999-9999", "(61) 99989-9999"],
        },
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"]== "Acesso Negado"

## post as public

def test_post_workstation_as_public(client:TestClient):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "adsl_vpn": False,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": False,
            "city_id": 1,
            "phones": ["(61) 99999-9999", "(61) 99989-9999"],
        },
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"]== "Acesso Negado"
