def test_delete_workstation(client):
    response = client.delete("/workstation/1")
    assert response.status_code == 200
    assert (
        response.json()["message"] == "Posto de trabalho removido com sucesso"
    )
    # verify = client.get("/workstation?workstation_id=1")
    # assert verify.status_code == 200
    # assert verify.json()["data"]["active"] == False


def test_delete_non_existing_workstation(client):
    response = client.delete("/workstation/90")
    assert response.status_code == 400
    assert response.json()["message"] == "Posto de trabalho não encontrado."
