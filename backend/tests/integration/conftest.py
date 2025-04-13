import asyncio
from contextlib import ExitStack
import pytest
import sys
from fastapi import Response
sys.path.append(sys.path[0] + '/../..')
print(sys.path[0])
from httpx import AsyncClient, ASGITransport
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor
import pytest_asyncio
from app import init_app
from app.users.model import User
from app.collection.model import Collection
from app.task.model import Task
from app.users.services import hash
from app.database import get_db, sessionmanager
from dotenv import load_dotenv
import os

load_dotenv()
version = os.getenv("API_VERSION")
test_url = "http://test/api/" + version

@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url=test_url) as c:
        yield c

test_db = factories.postgresql_proc(port=None, dbname="test_db")


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user, host=pg_host, port=pg_port, dbname=pg_db, version=test_db.version, password=pg_password
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()

@pytest_asyncio.fixture(scope='function', autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)
    
    
@pytest_asyncio.fixture(scope='function', autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
                yield session
    
    app.dependency_overrides[get_db] = get_db_override
    


@pytest_asyncio.fixture()
def get_test_user():
    return{
        "email":"test@test.com",
        "password":"test_pwd"
    }

@pytest_asyncio.fixture()
async def create_test_user(get_test_user):
    hashedpwd = hash(get_test_user['password'])
    user_instance = User(email = get_test_user['email'], password = hashedpwd)
    async with sessionmanager.session() as session:
        session.add(user_instance)
        await session.commit()
        await session.refresh(user_instance)

    return user_instance.id

@pytest_asyncio.fixture()
async def create_test_collection(create_test_user) ->Collection:
    collection_instance = Collection(collectionOwner_id = create_test_user, name="test_collection")
    async with sessionmanager.session() as session:
        session.add(collection_instance)
        await session.commit()
        await session.refresh(collection_instance)
    return collection_instance

@pytest_asyncio.fixture()
async def create_test_task(create_test_collection:Collection):
    task_instance = Task(collection_id = create_test_collection.id, name = "test_task")
    async with sessionmanager.session() as session:
        session.add(task_instance)
        await session.commit()
        await session.refresh(task_instance)
    return task_instance

@pytest_asyncio.fixture()
async def get_auth_header_for_user(client, create_test_user, get_test_user):
    response:Response = await client.post("/user/login", json=get_test_user)
    auth_header = response.headers.get("Authorization")
    return auth_header

    
