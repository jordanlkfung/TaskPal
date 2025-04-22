import pytest
from fastapi import status
from .conftest import Collection
@pytest.mark.asyncio
async def test_get_collection(client, create_test_collection, get_auth_header_for_user):
    response = await client.get(
        "collection/get",
        headers={"Authorization":get_auth_header_for_user}
    )
    
    assert response.status_code == status.HTTP_200_OK
    print(response.json())
    assert response.json() == [{'id': 1, 'name': 'test_collection'}]


@pytest.mark.asyncio
async def test_get_collection_unauthorized(client, get_invalid_auth_heater):
    response = await client.get(
        "collection/get",
        headers={"Authorization":get_invalid_auth_heater}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Unauthorized'}

@pytest.mark.asyncio
async def test_add_collection(client, get_auth_header_for_user):
    response = await client.post("collection/add",
                                 headers = {"Authorization":get_auth_header_for_user}
                                 ,json={"name":"test_collection_add"})
    
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_add_collection_unauthorized(client, get_invalid_auth_heater):
    response = await client.post("collection/add",
                                 headers = {"Authorization":get_invalid_auth_heater}
                                 ,json={"name":"test_collection_add"})
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Unauthorized'}

@pytest.mark.asyncio
async def test_update_collection(client, get_auth_header_for_user, create_test_collection:Collection):
    response = await client.patch('collection', headers = {"Authorization":get_auth_header_for_user},
                                  json={
                                      "name":"new name",
                                      "id":create_test_collection.id
                                  })
    

@pytest.mark.asyncio
async def test_update_collection_invalid_token(client, get_invalid_auth_heater, create_test_collection:Collection):
    response = await client.patch('collection', headers = {"Authorization":get_invalid_auth_heater})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Unauthorized'}

@pytest.mark.asyncio
async def test_update_collection_unauthorized_user():
    pass

@pytest.mark.asyncio
async def test_delete_collection(client, get_auth_header_for_user, create_test_collection:Collection):
    response = await client.delete(f'collection/{create_test_collection.id}', headers = {"Authorization":get_auth_header_for_user})
    

@pytest.mark.asyncio
async def test_delete_collection_unauthorized(client, get_invalid_auth_heater, create_test_collection:Collection):
    response = await client.delete(f"collection/{create_test_collection.id}",
                                   headers = {"Authorization":get_invalid_auth_heater})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Unauthorized'}
    

