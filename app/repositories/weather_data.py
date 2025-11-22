from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.weather_data import WeatherData
from app.repositories.base import BaseRepository


class WeatherDataRepository(BaseRepository[WeatherData]):
    def __init__(self, session: Session):
        super().__init__(session, WeatherData)

    def get_latest_by_city(self, city: str) -> WeatherData:
        return (
            (self.session.query(WeatherData).filter(WeatherData.location == city))
            .order_by(desc(WeatherData.created_at))
            .first()
        )
