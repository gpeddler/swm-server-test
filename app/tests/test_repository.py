import unittest
from sqlmodel import SQLModel, create_engine
from app.models import TodoValue
from app.repository import TodoRepository

DATABASE_URL = "sqlite:///./test_repo.db"
engine = create_engine(DATABASE_URL)


class TestTodoRepository(unittest.TestCase):
    def setUp(self):
        self.todo_repository = TodoRepository(engine)

        SQLModel.metadata.drop_all(engine)
        SQLModel.metadata.create_all(engine)

    # 성공: offset과 limit에 따라 Todo 목록을 조회한다.
    def test_list_todos_repository(self):
        todo_create1 = TodoValue(
            title="Test Todo 1", description="Description 1", completed=False
        )
        todo_create2 = TodoValue(
            title="Test Todo 2", description="Description 2", completed=True
        )

        self.todo_repository.create(todo_create1)
        self.todo_repository.create(todo_create2)

        # 성공: 기본 조건에서는 저장된 Todo를 모두 조회한다.
        todos = self.todo_repository.list()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].get_value(), todo_create1)
        self.assertEqual(todos[1].get_value(), todo_create2)

        # 성공: limit을 적용하면 요청한 개수만큼 조회한다.
        todos = self.todo_repository.list(limit=1)
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].get_value(), todo_create1)

        # 성공: offset을 적용하면 앞의 Todo를 건너뛰고 조회한다.
        todos = self.todo_repository.list(limit=1, offset=1)
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].get_value(), todo_create2)

        # 성공: offset이 전체 개수보다 크면 빈 목록을 조회한다.
        todos = self.todo_repository.list(limit=10, offset=10)
        self.assertEqual(len(todos), 0)

    # 성공: Todo를 저장하면 식별자가 부여된 Todo를 반환한다.
    def test_create_todo_repository(self):
        todo = self.todo_repository.create(
            TodoValue(
                title="Test Todo",
                description="This is a test todo item",
                completed=False,
            )
        )
        self.assertIsNotNone(todo.id)
        self.assertEqual(todo.title, "Test Todo")
        self.assertEqual(todo.description, "This is a test todo item")
        self.assertFalse(todo.completed)
