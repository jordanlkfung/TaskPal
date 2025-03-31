import unittest
import os
from fastapi.testclient import TestClient
import sys
# print(sys.path[0])
sys.path.append(sys.path[0] + '/..')
# print(sys.path[0])
from app import app
from app.database import get_db
from app.db_init import create_tables
from app.users.model import User

from sqlalchemy import select
# from app.database import get_db
# from app.db_init import create_tables
# from app import app
# from app.users.model import User
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi import status
from httpx import AsyncClient

import pytest



# Set up the in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"
# set datbase URL in env
BASE_URL = f'/api/{app.version}'
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# Create the tables in the test database

class TestUser(unittest.IsolatedAsyncioTestCase):

    @classmethod
    async def setUpClass(self):
        """Set up the app and the database for all tests."""
        self.original_env = os.environ.copy()
        os.environ['DB_URL'] = 'sqlite:///:memory:'
        self.db:AsyncSession = get_db()
        self.client = TestClient(app)
        create_tables()

        

    @classmethod
    async def tearDownClass(self):
        """Close the database session and clean up after tests."""
        # self.db.close()
        os.environ.clear()
        os.environ.update(self.original_env)

    async def test_default(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.json(), {"Health": "Good"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # async def test_add_user(self):
    #     '''Test the creation of task'''
    #     new_user = {"email":"test@email.com", "password":"test123"}

    #     response = self.client.post(f"{BASE_URL}/user/signup", json=new_user)
        
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json()['email'], new_user['email'])

    #     db  = await self.db.execute(select(User).where(User.email == new_user['email']))

    #     data = db.fetchone()

    #     self.assertEqual(response.json()['id'], data.id)
    

    # async def test_add_duplicate_email(self):
    #     new_user = {"email":"test@email.com", "password":"test123"}

    #     response = self.client.post(f"{BASE_URL}/user/signup", json=new_user)
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.json()['email'], new_user['email'])

    #     response = self.client.post(f"{BASE_URL}/user/signup", json=new_user)
    #     self.assertEqual(response.status_code, 400)
    #     #check that response message is correct
    #     self.assertEqual(response.json()['detail'], "Account already exists")

    #     db  = await self.db.execute(select(User).where(User.email == new_user['email']))

    #     data = db.fetchall()

    #     self.assertEqual(data.count, 1)
    
    # async def test_login(self):
    #     user_info = {"email":"test@gmail.com", "password":"password"}

    #     u_id = self.client.post(f"{BASE_URL}/signup", json=user_info)

    #     response = self.client.post(f"{BASE_URL}/login", json=user_info)

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.json()['email'], user_info["email"])
    #     self.assertEqual(response.json()['id'], u_id['id'])

    # async def test_login_no_account(self):
    #     user_info = {"email":"test@gmail.com", "password":"password"}
    #     response = self.client.post(f"{BASE_URL}/login", json=user_info)

    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    #     self.assertEqual(response.json()['detail'], "Invalid email or password")
        

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL)
test_async_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

async def override_get_db() -> AsyncSession:
    async with test_async_session_maker() as session:
        yield session

# Override the dependency for tests
app.dependency_overrides[get_db] = override_get_db       

@pytest.fixture(scope='function')
async def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()
    session = test_async_session_maker(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
async def test_client(db_session):
    async def override_get_db() -> AsyncSession:
        async with test_async_session_maker() as session:
            yield session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture()
def user_payload():
    return{
        "email":"test@test.com",
        "password":"password"
    }

@pytest.fixture()
async def test_add_user(test_client, user_payload):
    response = await test_client.post(f'{BASE_URL}/user', json= user_payload)

    assert response.status_code == status.HTTP_201_CREATED

if __name__ == "__main__":
    unittest.main()

