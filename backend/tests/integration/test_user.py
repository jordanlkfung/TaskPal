import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "user/signup",
        json={"email": "test@example.com", "password": "test"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Sign up successful"}

    response = await client.post(
        'user/login',
        json={"email": "test@example.com", "password": "test"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Login Successful",
    }

@pytest.mark.asyncio
async def test_login(client, get_test_user,create_test_user):
    response = await client.post(
        "/user/login", 
        json=get_test_user)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Login Successful",
    }

@pytest.mark.asyncio
async def test_signup_user_already_exists(client, get_test_user, create_test_user):
    response = await client.post(
        '/user/signup',
        json=get_test_user
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "detail": "Account already exists"
    }

@pytest.mark.asyncio
async def test_login_wrong_email(client, get_test_user, create_test_user):
    get_test_user['email'] = "test_wrong_email@gmail.com"
    response = await client.post(
        "/user/login",
        json = get_test_user
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid email or password"}

@pytest.mark.asyncio
async def test_login_incorrect_password(client, get_test_user, create_test_user):
    get_test_user['password'] = "incorrect_password"
    response = await client.post(
        "/user/login",
        json = get_test_user
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Invalid email or password"}