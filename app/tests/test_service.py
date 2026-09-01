import unittest
from unittest.mock import Mock

from app.exceptions import InvalidTodoTitleError
from app.models import Todo, TodoValue
from app.repository import TodoRepository
from app.service import TodoService


class TestTodoService(unittest.TestCase):
    def setUp(self):
        self.repository = Mock(spec=TodoRepository)
        self.todo_service = TodoService(self.repository)

    def test_list_todos_service(self):
        expected = [Todo(id=1, title="Test Todo")]
        self.repository.list.return_value = expected

        todos = self.todo_service.list(offset=5, limit=10)

        self.assertEqual(todos, expected)
        self.repository.list.assert_called_once_with(5, 10)

    def test_create_todo_service(self):
        todo_value = TodoValue(title="Test Todo", completed=False)
        expected = Todo(id=1, title="Test Todo", completed=False)
        self.repository.create.return_value = expected

        todo = self.todo_service.create(todo_value)

        self.assertEqual(todo, expected)
        self.repository.create.assert_called_once_with(todo_value)

    def test_create_todo_service_with_empty_title(self):
        todo_value = TodoValue(title="", completed=False)

        with self.assertRaises(InvalidTodoTitleError) as context:
            self.todo_service.create(todo_value)

        self.assertEqual(str(context.exception), "Title Field Required")
        self.repository.create.assert_not_called()
