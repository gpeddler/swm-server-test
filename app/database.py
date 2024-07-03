from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine


def get_engine(uri: str) -> Engine:
    return create_engine(uri, echo=True)


def init_db(engine: Engine):
    SQLModel.metadata.create_all(engine)
