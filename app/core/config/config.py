from app.core.config.base import BaseConfig
from app.core.config.db import DbBaseConfig
from app.core.config.weather_api import WeatherAPIConfig

__all__ = ["Settings", "settings"]


class Settings(BaseConfig):
    db: DbBaseConfig = DbBaseConfig()
    weather_api: WeatherAPIConfig = WeatherAPIConfig()


settings = Settings()
