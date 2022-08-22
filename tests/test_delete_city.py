def test_delete_city(client):
    response = client.delete("/city/10")
    assert response.status_code == 200
    assert (
        response.json()["message"] == "Cidade de id = 10 deletada com sucesso"
    )
    verify = client.get("/city?city_id=10")
    assert verify.status_code == 200
    assert not verify.json()["data"]


def test_delete_city_not_found(client):
    response = client.delete("/city/12")
    assert response.status_code == 200
    assert response.json()["message"] == "Cidade de id = 12 não encontrada"
