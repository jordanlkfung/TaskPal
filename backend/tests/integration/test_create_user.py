import pytest
from .conftest import test_url
from fastapi import Response

version = "v1"
base_url = f"{test_url}/api/{version}" 
user_url = base_url+"/user"
@pytest.mark.asyncio
async def test_create_user(client):
    response:Response = await client.get(f'{test_url}/healthcheck')
    assert response.status_code == 200
    assert response.json() == {"Health":"Good"}



    response = await client.post(
        f"{user_url}/signup",
        json={"email": "test@example.com", "password": "test"},
    )
    assert response.status_code == 201
    assert response.json() == {"message": "Sign up successful"}

    response = await client.post(
        'http://test/api/v1/user/login',
        json={"email": "test@example.com", "password": "test"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Login Successful",
    }
@pytest.mark.asyncio
async def test_login(client, get_test_user,create_test_user):
    response = await client.post(
        base_url+"/user/login", 
        json=get_test_user)
    assert response.status_code == 200
    assert response.json() == {
        "message": "Login Successful",
    }