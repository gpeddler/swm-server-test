from sqlmodel import SQLModel, Field
from typing import Optional


class TodoBase(SQLModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoValue(TodoBase):
    code: int
    message: str

    def fail_description_too_long(self):
        self.code = 422
        self.message = "Description is too long"
        return self
        


class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    def get_value(self) -> TodoValue:
        return TodoValue(
            title=self.title, description=self.description, completed=self.completed
        )
