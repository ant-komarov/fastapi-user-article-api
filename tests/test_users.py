import pytest
from fastapi.testclient import TestClient
from main import app
from db.models import User
from db.database import SessionLocal
from user.auth import AuthService


@pytest.fixture
def client():
    return TestClient(app)


USER_DATA = {
    "username": "Sam",  # Change name before testing
    "password": "john1234",
    "age": 31,
}
AGE = 30


def test_create_user(client):
    response = client.post("/users/sign-up", json=USER_DATA)

    assert response.status_code == 200
    response_data = response.json()

    assert "access_token" in response_data

    db = SessionLocal()
    created_user = db.query(User).filter(User.username == USER_DATA["username"]).first()
    db.close()

    assert created_user is not None
    assert created_user.username == USER_DATA["username"]
    assert created_user.age == USER_DATA["age"]


def test_get_users_with_param(client):
    db = SessionLocal()
    auth_service = AuthService(db=db)
    auth_token = auth_service.authenticate_user(
        USER_DATA["username"], USER_DATA["password"]
    ).access_token
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/users/?age={AGE}", headers=headers)
    user_names = [user["username"] for user in response.json()]

    assert response.status_code == 200
    assert USER_DATA["username"] in user_names

    user = db.query(User).filter(User.username == USER_DATA["username"]).first()
    db.delete(user)
    db.commit()
    db.close()
