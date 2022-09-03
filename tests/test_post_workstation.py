def test_post_workstation(client):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "asdl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": True,
            "city_id": 1,
            "phones": ["(61) 99999-9999", "(61) 99989-9999"],
        },
    )
    assert response.status_code == 201


def test_post_city_error(client):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "asdl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": True,
            "city_id": 50,
        },
    )
    assert response.status_code == 400


def test_post_regional_error(client):
    response = client.post(
        "/workstation",
        json={
            "name": "2ª DRP - Aparecida",
            "asdl_vpn": True,
            "link": "7ª DP  Aparecida",
            "ip": "10.11.1.1",
            "regional": False,
            "city_id": 5,
        },
    )
    assert response.status_code == 400
