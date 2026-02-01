from .utils import *
from ..routers.auth import get_db, get_current_user, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM # type: ignore
from jose import jwt
from datetime import timedelta, datetime, timezone
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user_success(test_user):
    db = TestSessionLocal()
    user = authenticate_user(test_user.username, "testpassword", db)
    assert user is not None
    assert user.username == test_user.username

    wrong_username = authenticate_user("wrongusername", "testpassword", db)
    assert wrong_username is False

    wrong_password = authenticate_user(test_user.username, "wrongpassword", db)
    assert wrong_password is False

def test_create_access_token(test_user):
    expires_delta = timedelta(minutes=15)
    token = create_access_token(
        username=test_user.username,
        user_id=test_user.id,
        role="admin",
        expires_delta=expires_delta
    )
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False})
    assert payload.get("sub") == test_user.username
    assert payload.get("id") == test_user.id
    assert payload.get("role") == "admin"

@pytest.mark.asyncio
async def test_get_current_user():
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token = token)

    assert user['username'] == 'testuser'   
    assert user['id'] == 1
    assert user['user_role'] == 'admin' 

@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'sub': 'testuser'}
    invalid_token = jwt.encode({}, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token = invalid_token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'


 