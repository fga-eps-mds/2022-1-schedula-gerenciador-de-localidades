def test_delete_workstation(client):
    response = client.delete("/workstation/2")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Posto de trabalho de id = 2 deletado com sucesso"
    )
    verify = client.get("/workstation?id=2")
    assert verify.status_code == 200
    assert verify.json()["message"] == "Dados não encontrados"
   

def test_delete_non_existing_workstation(client):
    response = client.delete("/workstation/90")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Nenhum posto de trabalho com id = 90 encontrado."
    )
