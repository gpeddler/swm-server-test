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

    def test_list_todos_repository(self):
        todo_create1 = TodoValue(
            title="Test Todo 1", description="Description 1", completed=False
        )
        todo_create2 = TodoValue(
            title="Test Todo 2", description="Description 2", completed=True
        )

        self.todo_repository.create(todo_create1)
        self.todo_repository.create(todo_create2)

        # ok - should return all list
        todos = self.todo_repository.list()
        self.assertEqual(len(todos), 2)
        self.assertEqual(todos[0].get_value(), todo_create1)
        self.assertEqual(todos[1].get_value(), todo_create2)

        # ok - should return first one
        todos = self.todo_repository.list(limit=1)
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].get_value(), todo_create1)

        # ok - should return second one
        todos = self.todo_repository.list(limit=1, offset=1)
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0].get_value(), todo_create2)

        # ok - should be empty
        todos = self.todo_repository.list(limit=10, offset=10)
        self.assertEqual(len(todos), 0)

    def test_create_todo_repository(self):
        # ok
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

        # error - empty title
        with self.assertRaises(ValueError) as context:
            todo = self.todo_repository.create(TodoValue(title="", completed=False))
        self.assertEqual(str(context.exception), "Title Field Required")
