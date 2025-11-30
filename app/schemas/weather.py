from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WeatherBase(BaseModel):
    location: str = Field(..., min_length=2, description="Name of the city")
    temperature: float = Field(..., description="Temperature in the city")
    humidity: float | None = Field(None, description="Humidity in the city")
    wind_speed: float | None = Field(None, description="Wind speed in the city")


class WeatherCreate(WeatherBase):
    pass


class WeatherDTO(WeatherBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
