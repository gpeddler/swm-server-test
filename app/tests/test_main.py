import unittest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from app.main import app
from app.database import get_engine

DATABASE_URL = "sqlite:///./test_main.db"
engine = create_engine(DATABASE_URL)


def override_get_engine():
    return engine


app.dependency_overrides[get_engine] = override_get_engine

client = TestClient(app)


class TestTodoAPI(unittest.TestCase):
    def setUp(self):
        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)

    def test_create_todo_api(self):
        response = client.post(
            "/api/todos/",
            json={
                "data": {
                    "title": "Test Todo",
                    "description": "This is a test todo item",
                    "completed": False,
                }
            },
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("data", data)

        data = data["data"]
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Test Todo")
        self.assertEqual(data["description"], "This is a test todo item")
        self.assertFalse(data["completed"])

    def test_list_todos_api(self):
        response = client.get("/api/todos/")
        self.assertEqual(response.status_code, 200)
