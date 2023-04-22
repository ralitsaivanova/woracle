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
