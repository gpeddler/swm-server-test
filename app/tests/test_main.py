import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.exceptions import InvalidTodoTitleError
from app.main import app, get_todo_service
from app.models import Todo, TodoValue
from app.service import TodoService


class TestTodoAPI(unittest.TestCase):
    def setUp(self):
        self.todo_service = Mock(spec=TodoService)
        app.dependency_overrides[get_todo_service] = lambda: self.todo_service
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides.clear()

    # 성공: 올바른 요청을 보내면 생성된 Todo를 응답한다.
    def test_create_todo_api(self):
        self.todo_service.create.return_value = Todo(
            id=1,
            title="Test Todo",
            description="This is a test todo item",
            completed=False,
        )

        response = self.client.post(
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
        self.assertEqual(
            response.json(),
            {
                "data": {
                    "id": 1,
                    "title": "Test Todo",
                    "description": "This is a test todo item",
                    "completed": False,
                }
            },
        )
        self.todo_service.create.assert_called_once_with(
            TodoValue(
                title="Test Todo",
                description="This is a test todo item",
                completed=False,
            )
        )

    # 예외: 제목이 비어 있으면 422 상태와 제목 필수 오류를 응답한다.
    def test_create_todo_api_with_empty_title(self):
        self.todo_service.create.side_effect = InvalidTodoTitleError()

        response = self.client.post(
            "/api/todos/",
            json={"data": {"title": "", "completed": False}},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": "Title Field Required"})

    # 성공: Todo가 없으면 빈 목록을 응답한다.
    def test_list_todos_api(self):
        self.todo_service.list.return_value = []

        response = self.client.get("/api/todos/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"data": []})
        self.todo_service.list.assert_called_once_with(0, 10)
