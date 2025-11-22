from sqlalchemy import Column, DateTime, Float, String, func

from app.models.base import BaseModel


class WeatherData(BaseModel):
    __tablename__ = "weather_data"

    location = Column(String(255), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)

    created_at = Column(
        DateTime, default=func.now(), server_default=func.now(), index=True
    )
