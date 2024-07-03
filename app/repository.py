from typing import List, Optional
from sqlalchemy import Engine
from sqlmodel import Session, select
from .models import Todo, TodoValue


class TodoRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def list(self, offset: int = 0, limit: int = 10) -> List[Todo]:
        with Session(self.engine) as session:
            todos = session.exec(select(Todo).offset(offset).limit(limit)).all()
            return todos

    def create(self, todo_value: TodoValue) -> Todo:
        if len(todo_value.title) == 0:
            raise ValueError("Title Field Required")

        with Session(self.engine) as session:
            todo = Todo.model_validate(todo_value)
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return todo
