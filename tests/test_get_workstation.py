def test_get_workstation(client):
    url = "/workstation"
    response = client.get(url)
    assert response.status_code == 200


def test_get_workstation_id(client):
    url = "/workstation?id=1"
    response = client.get(url)
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
        "active": True,
        "phones": [
            {
                "id": 1,
                "number": "16549841",
                "workstation_id": 1
            }
        ]
    }


def test_workstation_id_not_found(client):
    response = client.get("/workstation?id=12")
    assert response.status_code == 200
    assert response.json()["message"] == "Dados não encontrados"
