def test_root(fastapi_client):
    response = fastapi_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Woracle"}


def test_adding_cake_sucessfully(fastapi_client, test_db):
    input_params = {
        "name": "Aranygaluska",
        "comment": "A cake with yeasty dough and vanilla custard.",
        "imageUrl": "http://www.aranygaluska.com/",
        "yumFactor": 1,
    }

    response = fastapi_client.post("/cakes/", json=input_params)
    assert response.status_code == 201
    assert response.json()["name"] == input_params["name"]
    assert response.json()["comment"] == input_params["comment"]
    assert response.json()["imageUrl"] == input_params["imageUrl"]
    assert response.json()["yumFactor"] == input_params["yumFactor"]


def test_adding_cake_fails_validation(fastapi_client, test_db):
    input_params = {
        "name": "Thisvalueistoolongsoitshouldreturnanerror",
        "comment": "A cake with yeasty dough and vanilla custard.",
        "imageUrl": "not-a-url",
        "yumFactor": 999,
    }

    response = fastapi_client.post("/cakes/", json=input_params)

    assert response.status_code == 422
    error_details = response.json()["detail"]

    for error_detail in error_details:
        if error_detail["loc"][1] == "name":
            assert error_detail["msg"] == "ensure this value has at most 30 characters"
        if error_detail["loc"][1] == "imageUrl":
            assert error_detail["msg"] == "invalid or missing URL scheme"
        if error_detail["loc"][1] == "yumFactor":
            assert error_detail["msg"] == "ensure this value is less than or equal to 5"


def test_list_cake_empty(fastapi_client, test_db):
    response = fastapi_client.get("/cakes/")

    assert response.status_code == 200
    assert response.json() == []


def test_list_cake_has_entries(fastapi_client, test_db):
    input_params = {
        "name": "Black Bun",
        "comment": "A dense and rich fruit cake often used for the ritual of first-footing at Hogmanay.",
        "imageUrl": "http://www.blackbun.com/",
        "yumFactor": 3,
    }
    # add a cake to find in the list
    response = fastapi_client.post("/cakes/", json=input_params)
    assert response.status_code == 201

    # get the list of cakes
    response = fastapi_client.get("/cakes/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == 1
    assert response.json()[0]["name"] == input_params["name"]
    assert response.json()[0]["comment"] == input_params["comment"]
    assert response.json()[0]["imageUrl"] == input_params["imageUrl"]
    assert response.json()[0]["yumFactor"] == input_params["yumFactor"]

    # add another cake
    input_params = {
        "name": "Millionaire Shortbread",
        "comment": "A shortbread biscuit base topped with caramel and milk chocolate.",
        "imageUrl": "http://www.millionaire.com/",
        "yumFactor": 5,
    }
    response = fastapi_client.post("/cakes/", json=input_params)
    assert response.status_code == 201

    # get the list of cakes again
    response = fastapi_client.get("/cakes/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_delete_inexistent_id_returns_404(fastapi_client, test_db):
    response = fastapi_client.delete("/cakes/33/")
    assert response.status_code == 404


def test_delete_cake_successfully(fastapi_client, test_db):
    input_params = {
        "name": "Victoria Sponge",
        "comment": "a baking classic and a tasty tea-time treat",
        "imageUrl": "http://www.victoriasponge.com/",
        "yumFactor": 4,
    }
    # add a cake to find in the list
    response = fastapi_client.post("/cakes/", json=input_params)
    assert response.status_code == 201

    cake_id = response.json()["id"]

    response = fastapi_client.delete(f"/cakes/{cake_id}/")
    assert response.status_code == 204
