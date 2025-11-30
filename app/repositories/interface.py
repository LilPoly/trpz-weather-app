from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

T = TypeVar("T")


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T:
        pass

    @abstractmethod
    def find(self, predicate: Callable[..., bool]) -> list[T]:
        pass

    @abstractmethod
    def add(self, item: T) -> T:
        pass

    @abstractmethod
    def update(self, item: T) -> T:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
