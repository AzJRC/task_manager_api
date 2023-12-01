import pytest
from fastapi.testclient import TestClient
from app.main import app

"Execute command: pytest -s -v --disable-warnings -l"

client = TestClient(app)

# Test root enpoint to verify that the API is working 
def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# Test user creation and login

test_user = {
    "username": "pytest_user",
    "email": "pytest_user@gmail.com",
    "password": "12345"
}

test_user_response = {
    "operation": "successful",
    "user_details": {
        "username": "pytest_user",
        "email": "pytest_user@gmail.com",
        "user_state": True
    }
}

def test_create_new_user():
    response = client.post("/users/", json=test_user)
    assert response.status_code == 200
    assert response.json() == test_user_response


def test_same_user_again():
    response = client.post("/users/", json=test_user)
    assert response.status_code == 403
    assert response.json() == {'detail': 'User already exists.'}


test_user_login = {
    "username": "pytest_user",
    "password": "12345"
}

def test_login_user(): # Use this function to get the autorization headers
    response = client.post("/login/", data=test_user_login)
    token = response.json()
    token_header = token["token_type"] + " " + token["access_token"]
    assert response.status_code == 200
    return {"Authorization": token_header}


def test_delete_user():
    response = client.delete("/users/", headers=test_login_user())
    assert response.status_code == 204