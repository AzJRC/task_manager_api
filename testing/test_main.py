import pytest
from fastapi.testclient import TestClient
from app.main import app

"Execute command: pytest --disable-warnings --no-summary -l -v"

client = TestClient(app)

# Test root enpoint to verify that the API is working 
def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


user_sample = {
    "username": "pytest_user",
    "email": "pytest_user@gmail.com",
    "password": "12345"
}

user_response_sample = {
    "operation": "successful",
    "user_details": {
        "username": "pytest_user",
        "email": "pytest_user@gmail.com",
        "user_state": True
    }
}

user2_sample = {
    "username": "pytest_user2",
    "email": "pytest_user2@gmail.com",
    "password": "12345"
}

def test_create_new_user():
    response = client.post("/users/", json=user_sample)
    assert response.status_code == 200
    assert response.json() == user_response_sample


def test_create_another_user():
    response = client.post("/users/", json=user2_sample)
    assert response.status_code == 200


user_login_sample = {
    "username": "pytest_user",
    "password": "12345"
}

user2_login_sample = {
    "username": "pytest_user2",
    "password": "12345"
}

def test_login_user(user: dict = user_login_sample): # Use this function to get the autorization headers
    response = client.post("/login/", data = user)
    token = response.json()
    token_header = token["token_type"] + " " + token["access_token"]
    assert response.status_code == 200
    return {"Authorization": token_header}


def test_get_current_user(user_credentials: dict = user_login_sample): # Use this function to get user's details
    response = client.get("/users/me", headers=test_login_user(user_credentials))
    assert response.status_code == 200
    user =  response.json()
    return user


task_sample = {
    "title": "taks title",
    "description": "hello world"
}

def test_create_task():
    response = client.post("/tasks/", headers=test_login_user(), json=task_sample)
    assert response.status_code == 200


def test_get_user_tasks(): # Use this function to get current user's tasks
    response = client.get("/tasks/", headers=test_login_user())
    assert response.status_code == 200
    return response.json()
    

# Deletion tests


def test_delete_task():
    tasks = test_get_user_tasks()[0]
    task_id = tasks["id"]
    response = client.delete("/tasks/{}/".format(task_id), headers=test_login_user())
    assert response.status_code == 204


def test_delete_user():
    response = client.delete("/users/", headers=test_login_user())
    assert response.status_code == 204

user2_login_sample = {
    "username": "pytest_user2",
    "password": "12345"
}

def test_delete_user2():
    response = client.delete("/users/", headers=test_login_user(user2_login_sample))
    assert response.status_code == 204