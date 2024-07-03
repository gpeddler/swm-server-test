from typing import List
from pydantic import BaseModel

from app.models import Todo, TodoValue


class ListTodoResponse(BaseModel):
    data: List[Todo]


class CreateTodoRequest(BaseModel):
    data: TodoValue


class CreateTodoResponse(BaseModel):
    data: Todo
