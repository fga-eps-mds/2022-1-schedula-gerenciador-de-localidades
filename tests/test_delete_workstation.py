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
    # assert verify.json()["data"] == {
    #     "id": 2,
    #     "city_id": 1,
    #     "name": "2ª DP de Goiânia",
    #     "ip": "127.0.0.0",
    #     "link": "exemplo de link",
    #     "adsl_vpn": True,
    #     "regional": False,
    #     "regional_id": 1,
    #     "active": False,
    #     "phones": []
    # }


def test_delete_non_existing_workstation(client):
    response = client.delete("/workstation/90")
    assert response.status_code == 200
    assert (
        response.json()["message"]
        == "Nenhum posto de trabalho com id = 90 encontrado."
    )
