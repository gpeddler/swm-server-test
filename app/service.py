from app.exceptions import DuplicateTodoTitleError, InvalidTodoTitleError
from app.models import Todo, TodoValue
from app.repository import TodoRepository


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def list(self, offset: int = 0, limit: int = 10) -> list[Todo]:
        return self.repository.list(offset, limit)

    def create(self, todo_value: TodoValue) -> Todo:
        todo_value.title = todo_value.title.strip()

        if not todo_value.title:
            raise InvalidTodoTitleError()

        existing_todos = self.repository.find_by_completed_and_title(
            False, todo_value.title
        )
        if existing_todos:
            raise DuplicateTodoTitleError()

        return self.repository.create(todo_value)
