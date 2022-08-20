def test_get_city(client):
    url = "/city"
    response = client.get(url)
    assert response.status_code == 200


def test_get_cityid(client):
    url = "/city?city_id=2"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()["data"] == {
        "id": 2,
        "name": "Cidade 2",
    }


def test_city_id_not_found(client):
    response = client.get("/city?city_id=12")
    assert response.status_code == 200
    assert response.json()["message"] == "Nenhuma cidade encontrada"
