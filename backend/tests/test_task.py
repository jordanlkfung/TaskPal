import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..app.database import Base, get_db
from ..app import app
from ..app.task.schemas import TaskPriority, addTaskSchema
from ..app.task.routes import task_router
from ..app.task.service import TaskService
from ..app.db_init import create_tables

# Set up the in-memory SQLite database for testing
# DATABASE_URL = "sqlite:///:memory:"
BASE_URL = f'/api/{app.version}'
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables in the test database
create_tables()


class TestTask(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Set up the app and the database for all tests."""
        self.db = get_db()
        self.client = TestClient(app)

    @classmethod
    def tearDownClass(self):
        """Close the database session and clean up after tests."""
        self.db.close()

    def test_create_item(self):
        """Test the creation of an item."""
        item_data = {"name": "Test Item", "description": "Test Description"}
        
        # Send POST request to create an item
        response = self.client.post("/items/", json=item_data)
        
        # Assertions to ensure the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], item_data["name"])
        self.assertEqual(response.json()["description"], item_data["description"])
        
        # Check if the item was actually added to the database
        db_item = self.db.query(Item).filter(Item.name == "Test Item").first()
        self.assertIsNotNone(db_item)
        self.assertEqual(db_item.name, item_data["name"])

    def test_create_item_missing_name(self):
        """Test the creation of an item with missing name."""
        item_data = {"description": "Test Description"}
        
        response = self.client.post("/items/", json=item_data)
        
        # Check for proper error response (e.g., validation error)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity
        self.assertIn("detail", response.json())
    
    def test_create_task(self):
        '''Test the creation of task'''
        new_item = addTaskSchema("Test task")

        response = self.client.post("")
        

if __name__ == "__main__":
    unittest.main()
