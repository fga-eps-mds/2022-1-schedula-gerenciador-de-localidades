def test_put_city(client):
    response = client.put(
        "/city/1", json={"name": "new test"}
    )
    assert response.status_code == 200


def test_put_city_invalid_name(client):
    response = client.put(
        "/city/1", json={"name": None}
    )
    assert response.status_code == 422


def test_put_invalid_city(client):
    response = client.put(
        "/city/12", json={"name": "test"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Cidade não encontrada"
