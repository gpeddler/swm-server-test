from typing import Annotated, Optional
from fastapi import Depends, FastAPI

from app.api_models import CreateTodoRequest, CreateTodoResponse, ListTodoResponse
from app.repository import TodoRepository
from app.settings import Settings
from app import database

app = FastAPI()
settings = Settings()

# database
engine = database.get_engine(settings.DATABASE_URL)
database.init_db(engine)


# repository
def get_todo_repository():
    return TodoRepository(engine)


@app.get("/")
async def health_check():
    return {}


@app.get("/api/todos/", response_model=ListTodoResponse)
async def list_todo(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    repo: TodoRepository = Depends(get_todo_repository),
):
    return ListTodoResponse(data=repo.list(offset, limit))


@app.post("/api/todos/", response_model=CreateTodoResponse)
async def create_todo(
    req: CreateTodoRequest,
    repo: TodoRepository = Depends(get_todo_repository),
):
    return CreateTodoResponse(data=repo.create(req.data))
