from typing import Type, TypeVar

from sqlalchemy.orm import Session

from app.models.base import BaseModel
from app.repositories.interface import IGenericRepository

T = TypeVar("T", bound=BaseModel)


class BaseRepository(IGenericRepository[T]):
    def __init__(self, session: Session, model_type: Type[T]):
        self.session = session
        self.model = model_type

    def get_all(self) -> list[T]:
        return self.session.query(self.model).all()

    def get_by_id(self, id: int) -> T:
        return self.session.get(self.model, id)

    def find(self, predicate: any) -> list[T]:
        return self.session.query(self.model).filter(predicate).all()

    def add(self, item: T) -> T:
        self.session.add(item)
        self.session.flush()
        self.session.refresh(item)
        return item

    def update(self, item: T) -> T:
        updated_item = self.session.merge(item)
        self.session.flush()
        return updated_item

    def delete(self, id: int) -> None:
        item = self.get_by_id(id)
        if item:
            self.session.delete(item)
            self.session.flush()
