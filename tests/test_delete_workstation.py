from fastapi.testclient import TestClient

from utils.auth_utils import ADMIN_HEADER, BASIC_HEADER, MANAGER_HEADER


def test_delete_workstation_as_admin(client: TestClient):
    response = client.delete("/workstation/1", headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert (
        response.json()["message"] == "Posto de trabalho removido com sucesso"
    )
    # verify = client.get("/workstation?workstation_id=1")
    # assert verify.status_code == 200
    # assert verify.json()["data"]["active"] == False


def test_delete_non_existing_workstation_as_admin(client: TestClient):
    response = client.delete("/workstation/90", headers=ADMIN_HEADER)
    assert response.status_code == 400
    assert response.json()["message"] == "Posto de trabalho não encontrado."


def test_delete_workstation_as_manager(client: TestClient):
    response = client.delete("/workstation/1", headers=MANAGER_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_workstation_as_basic(client: TestClient):
    response = client.delete("/workstation/1", headers=BASIC_HEADER)
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"


def test_delete_workstation_as_public(client: TestClient):
    response = client.delete("/workstation/1")
    assert response.status_code == 401
    assert response.json()["message"] == "Acesso negado"
