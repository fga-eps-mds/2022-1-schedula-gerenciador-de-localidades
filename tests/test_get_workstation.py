def test_get_workstation(client):
    url = "/workstation"
    response = client.get(url)
    assert response.status_code == 200


def test_get_workstation_by_regional(client):
    url = "/workstation?regional=True"
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_workstationid(client):
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
        "active": False,
        "phones": [],
    }


def test_workstation_id_not_found(client):
    response = client.get("/workstation?id=12")
    assert response.status_code == 200
    assert response.json()["message"] == "Dados não encontrados"
