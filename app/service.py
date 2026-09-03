from app.exceptions import InvalidTodoTitleError
from app.models import Todo, TodoValue
from app.repository import TodoRepository


class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def list(self, offset: int = 0, limit: int = 10) -> list[Todo]:
        return self.repository.list(offset, limit)

    def create(self, todo_value: TodoValue) -> Todo:
        if not todo_value.title:
            raise InvalidTodoTitleError()
        
        if len(todo_value.description) > 200:
            return todo_value.fail_description_too_long()
            
        return self.repository.create(todo_value)
