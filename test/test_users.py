from .utils import *
from ..routers.users import get_db, get_current_user  # type: ignore
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_users_authenticated(test_user):
    response = client.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() == [{'id': 1, 'username': 'testuser', 
    # 'email': 'testuser@example.com'}]
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == "testuser@example.com"


def test_change_password_success(test_user):
    response = client.put("/user/password", json={
        "password": "testpassword",
        "new_password": "newtestpassword"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # assert response.json() == {"detail": "Password updated successfully."}

def test_change_password_failure_wrong_current_password(test_user):
    response = client.put("/user/password", json={
        "password": "wrongpassword",
        "new_password": "newtestpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change"}




