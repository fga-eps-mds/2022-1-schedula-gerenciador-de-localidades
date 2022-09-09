from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_put_workstation_as_admin(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999"],
        },
        headers=ADMIN_HEADER
    )

    assert response.json()["message"] == "Dado atualizado com sucesso"
    assert response.status_code == 200

    # verify = client.get("workstation/1")
    # assert verify.json()["data"] == {
    #     "name": "teste",
    #     "adsl_vpn": true,
    #     "link": "teste",
    #     "ip": "10.11.1.1",
    #     "regional": true,
    #     "city_id": 1
    # }


def test_put_non_existing_workstation_as_admin(client: TestClient):
    response = client.put(
        "workstation/90",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
        },
        headers=ADMIN_HEADER
    )

    assert (
        response.json()["message"]
        == "O Posto de Trabalho não está cadastrado."
    )
    assert response.status_code == 400


def test_put_workstation_without_regional_as_admin(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": False,
            "city_id": 1,
        },
        headers=ADMIN_HEADER
    )
    assert (
        response.json()["message"]
        == "Caso o posto de trabalho não seja regional, forneça a regional à qual ele pertence."  # noqa E501
    )
    assert response.status_code == 400


def test_put_workstation_with_non_existing_city_as_admin(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 50,
        },
        headers=ADMIN_HEADER
    )
    assert response.json()["message"] == "A cidade não está cadastrada."
    assert response.status_code == 400


def teste_workstation_duplicity_as_admin(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "3ª DP de Luziânia",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 5,
        },
        headers=ADMIN_HEADER
    )
    assert response.json()["message"] == "Erro ao processar dados"
    assert response.status_code == 500


def test_put_workstation_as_manager(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999"],
        },
        headers=MANAGER_HEADER
    )

    assert response.json()["message"] == "Dado atualizado com sucesso"
    assert response.status_code == 200


def test_put_workstation_as_basic(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999"],
        },
        headers=BASIC_HEADER
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_put_workstation_as_public(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999"],
        }
    )
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
