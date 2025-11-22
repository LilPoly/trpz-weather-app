from sqlalchemy.orm import Session

from app.database.postgres import SessionFactory
from app.repositories.user import UserRepository
from app.repositories.weather_data import WeatherDataRepository


class UnitOfWork:
    def __init__(self):
        self.session_factory = SessionFactory
        self.session: Session = None

        self._user_repository: UserRepository = None
        self._weather_repository: WeatherDataRepository = None

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
            self.close()
            return False
        self.close()

    @property
    def user(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository(self.session)
        return self._user_repository

    @property
    def weather(self) -> WeatherDataRepository:
        if self._weather_repository is None:
            self._weather_repository = WeatherDataRepository(self.session)
        return self._weather_repository

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def close(self):
        if self.session:
            self.session.close()
