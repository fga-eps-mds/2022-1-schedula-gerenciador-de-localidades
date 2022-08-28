from fastapi.testclient import TestClient


def test_put_workstation(client: TestClient):
    response = client.put(
        "workstation/3",
        json={
            "name": "teste",
            "adsl_vpn": True,
            "regional": True,
            "city_id": 1,
            "phones": [
                {
                    "number": "111"
                }
            ]
        },
    )
    assert response.json()["message"] == "Dados alterados com sucesso"
    assert response.status_code == 200
    verify = client.get("workstation?id=3")
    assert verify.json()["data"] == {
        "id": 3,
        "city_id": 1,
        "name": "teste",
        "ip": "127.0.0.0",
        "link": "exemplo de link",
        "adsl_vpn": True,
        "regional": True,
        "regional_id": None,
        "active": True,
        "phones": [{
            "number": "111",
            "workstation_id": 3,
            "id": 10

        }]
    }


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
        == "O Posto de Trabalho de id = 90 não está cadastrado."
    )
    assert response.status_code == 200


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
        == "Caso o posto de trabalho não seja regional, forneça o a regional à qual ele pertence."  # noqa E501
    )
    assert response.status_code == 200


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
    assert (
        response.json()["message"]
        == "A cidade de id = 50 não está cadastrada."
    )
    assert response.status_code == 200


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
