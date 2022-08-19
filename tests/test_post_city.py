def test_post_city(client):
    response = client.post(
        "/city",
        json={"name": "test"},
    )
    assert response.status_code == 201


def test_post_city_invalid_name(client):
    response = client.post(
        "/city", json={"name": None},
    )
    assert response.status_code == 422
