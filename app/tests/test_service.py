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

    # 성공: 목록 조회 조건을 Repository에 전달하고 조회 결과를 반환한다.
    def test_list_todos_service(self):
        expected = [Todo(id=1, title="Test Todo")]
        self.repository.list.return_value = expected

        todos = self.todo_service.list(offset=5, limit=10)

        self.assertEqual(todos, expected)
        self.repository.list.assert_called_once_with(5, 10)

    # 성공: 유효한 Todo를 Repository에 전달하고 생성 결과를 반환한다.
    def test_create_todo_service(self):
        todo_value = TodoValue(title="Test Todo", completed=False)
        expected = Todo(id=1, title="Test Todo", completed=False)
        self.repository.create.return_value = expected

        todo = self.todo_service.create(todo_value)

        self.assertEqual(todo, expected)
        self.repository.create.assert_called_once_with(todo_value)

    # 예외: 제목이 비어 있으면 전용 예외를 발생시키고 저장하지 않는다.
    def test_create_todo_service_with_empty_title(self):
        todo_value = TodoValue(title="", completed=False)

        with self.assertRaises(InvalidTodoTitleError) as context:
            self.todo_service.create(todo_value)

        self.assertEqual(str(context.exception), "Title Field Required")
        self.repository.create.assert_not_called()
