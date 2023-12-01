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


def test_get_user_tasks():
    response = client.get("/tasks/", headers=test_login_user())
    assert response.status_code == 200


def test_get_task_by_title():
    response = client.get("/tasks/taks%20title", headers=test_login_user())
    assert response.status_code == 200


user_group_sample = {
    "group_name": "test user group",
    "group_description": "hello world!"
}

def test_create_user_group():
    response = client.post("/user_groups/", headers=test_login_user(), json=user_group_sample)
    assert response.status_code == 200


def test_get_group_by_title():
    response = client.get("/user_groups/test%20user%20group", headers=test_login_user())
    assert response.status_code == 200
    return response.json()

member_sample = {
    "member_id": 0, #replace with current user2_id -> member_sample["member_id"] = user2_id
    "member_role": 3
}

def test_add_member_to_user_group():
    user2 = test_get_current_user(user_credentials=user2_login_sample)
    user2_id = user2["id"]
    group = test_get_group_by_title()
    group_id = group["id"]
    member_sample["member_id"] = user2_id  # Set the member_id in the dictionary

    response = client.post("/user_groups/{}".format(group_id), 
                           headers=test_login_user(), 
                           json=member_sample)
    assert response.status_code == 204
    print(test_get_group_by_title())



# Deletion tests

def test_delete_user_group():
    pass


def test_delete_task():
    response = client.delete("/tasks/taks%20title", headers=test_login_user())
    response.status_code == 204


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