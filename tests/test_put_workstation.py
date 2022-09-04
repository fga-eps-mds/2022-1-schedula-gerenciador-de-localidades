from fastapi.testclient import TestClient


def test_put_workstation(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999"],
        },
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


def test_put_non_existing_workstation(client: TestClient):
    response = client.put(
        "workstation/90",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
        },
    )

    assert (
        response.json()["message"]
        == "O Posto de Trabalho não está cadastrado."
    )
    assert response.status_code == 400


def test_put_workstation_without_regional(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": False,
            "city_id": 1,
        },
    )
    assert (
        response.json()["message"]
        == "Caso o posto de trabalho não seja regional, forneça a regional à qual ele pertence."  # noqa E501
    )
    assert response.status_code == 400


def test_put_workstation_with_non_existing_city(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 50,
        },
    )
    assert response.json()["message"] == "A cidade não está cadastrada."
    assert response.status_code == 400


def teste_workstation_duplicity(client: TestClient):
    response = client.put(
        "workstation/1",
        json={
            "name": "3ª DP de Luziânia",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 5,
        },
    )
    assert response.json()["message"] == "Erro ao processar dados"
    assert response.status_code == 500
