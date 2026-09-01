from typing import Optional

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from app import database
from app.api_models import CreateTodoRequest, CreateTodoResponse, ListTodoResponse
from app.exceptions import InvalidTodoTitleError
from app.repository import TodoRepository
from app.service import TodoService
from app.settings import Settings

app = FastAPI()
settings = Settings()

# database
engine = database.get_engine(settings.DATABASE_URL)
database.init_db(engine)


# repository
def get_todo_repository():
    return TodoRepository(engine)


def get_todo_service(
    repository: TodoRepository = Depends(get_todo_repository),
):
    return TodoService(repository)


@app.exception_handler(InvalidTodoTitleError)
async def handle_invalid_todo_title(_request: Request, error: InvalidTodoTitleError):
    return JSONResponse(status_code=422, content={"detail": str(error)})


@app.get("/")
async def health_check():
    return {}


@app.get("/api/todos/", response_model=ListTodoResponse)
async def list_todo(
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    service: TodoService = Depends(get_todo_service),
):
    return ListTodoResponse(data=service.list(offset, limit))


@app.post("/api/todos/", response_model=CreateTodoResponse)
async def create_todo(
    req: CreateTodoRequest,
    service: TodoService = Depends(get_todo_service),
):
    return CreateTodoResponse(data=service.create(req.data))
