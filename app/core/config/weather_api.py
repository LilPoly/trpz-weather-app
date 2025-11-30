from pydantic import Field

from app.core.config.base import BaseConfig


class WeatherAPIConfig(BaseConfig):
    GEO_URL: str = Field(..., description="Geo URL")
    WEATHER_URL: str = Field(..., description="Weather URL")
