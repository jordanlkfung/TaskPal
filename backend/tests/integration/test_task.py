import pytest
from .conftest import Collection
from fastapi import status
@pytest.mark.asyncio
async def test_get_tasks(client, get_auth_header_for_user, create_test_collection:Collection):
    response = await client.get(f'task/{create_test_collection.id}',
                                headers={"Authorization":get_auth_header_for_user})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def tast_get_tasks_collection_doesnt_exist(client, get_auth_header_for_user):
    response = await client.get(f'task/0',
                                headers = {"Authorization":get_auth_header_for_user})
    
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_get_tasks_unauthorized_user(client, create_test_collection, get_auth_header_for_second_user):
    response = await client.get(f'task/{create_test_collection.id}',
                                headers ={"Authorization":get_auth_header_for_second_user})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_get_tasks_missing_token(client, get_invalid_auth_heater, create_test_collection):
    response = await client.get(f'task/{create_test_collection.id}',
                                headers ={"Authorization":get_invalid_auth_heater})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_create_task(client, get_auth_header_for_user, create_test_collection):
    response = await client.post(f'task/add',
                                 json={
                                "name": "add task",
                                "collection_id": create_test_collection.id
                                },
                                headers = {"Authorization":get_auth_header_for_user})
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.asyncio
async def test_create_task_invalid_priority(client, get_auth_header_for_user, create_test_collection):
    response = await client.post(f'task/add',
                                 json={
                                "name": "add task",
                                "priority":10,
                                "collection_id": create_test_collection.id
                                },
                                headers = {"Authorization":get_auth_header_for_user})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_create_task_collection_doesnt_exist(client,get_auth_header_for_user):
    response = await client.post(f'task/add',
                                 json={
                                "name": "add task",
                                "priority":1,
                                "collection_id": 0
                                },
                                headers = {"Authorization":get_auth_header_for_user})
    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.asyncio
async def test_create_task_unauthorized_user(client, get_auth_header_for_second_user, create_test_collection):
    response = await client.post(f'task/add',
                                 json={
                                "name": "add task",
                                "collection_id": create_test_collection.id
                                },
                                headers = {"Authorization":get_auth_header_for_second_user})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_create_task_missing_token(client, get_invalid_auth_heater):
    response = await client.post(f'task/add',
                                 json={
                                "name": "add task",
                                "collection_id": 0
                                },
                                headers = {"Authorization":get_invalid_auth_heater})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_update_task(client, create_test_task, get_auth_header_for_user):
    response = await client.patch(f'task/',
                                  headers = {"Authorization":get_auth_header_for_user},
                                  json={
                                    "name": "string",
                                    "priority": 0,
                                    "id": create_test_task.id
                                    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
@pytest.mark.asyncio
async def test_update_task_invalid_priority(client, create_test_task, get_auth_header_for_user):
    response = await client.patch(f'task/',
                                  headers = {"Authorization":get_auth_header_for_user},
                                  json={
                                    "name": "string",
                                    "priority": 10,
                                    "id": create_test_task.id
                                    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_update_task_invalid_task_id(client, create_test_task, get_auth_header_for_user):
    response = await client.patch(f'task/',
                                  headers = {"Authorization":get_auth_header_for_user},
                                  json={
                                    "name": "string",
                                    "priority": 10,
                                    "id": 100
                                    })
    assert response.status_code == status.HTTP_404_NOT_FOUND 
@pytest.mark.asyncio
async def test_update_task_unauthorized_user(client,create_test_task, get_auth_header_for_second_user):
    response = await client.patch('task/',
                                  headers = {"Authorization":get_auth_header_for_second_user},
                                  json={
                                    "name": "string",
                                    "priority": 1,
                                    "id": create_test_task.id
                                    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_update_task_invalid_token(client, get_invalid_auth_heater):
    response = await client.patch('task/',
                                  headers = {"Authorization":get_invalid_auth_heater},
                                  json={
                                    "name": "string",
                                    "priority": 1,
                                    "id": 0
                                    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.asyncio
async def test_delete_task(client,create_test_task,get_auth_header_for_user):
    response = await client.delete(f"/task/{create_test_task.id}",
                                   headers={"Authorization": get_auth_header_for_user})
    
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.asyncio
async def test_delete_task_missing_headers():
    pass

@pytest.mark.asyncio
async def test_delete_task_task_does_not_exist():
    pass

@pytest.mark.asyncio
async def test_delete_task_unauthorized_user():
    pass

@pytest.mark.asyncio
async def test_delete_task_invalid_token():
    pass