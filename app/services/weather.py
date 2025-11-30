import matplotlib.pyplot as plt
import openmeteo_requests
import pandas as pd
import requests
import requests_cache
from loguru import logger
from retry_requests import retry

from app.core.config.config import settings
from app.core.context import SecurityContext
from app.models.weather_data import WeatherData
from app.schemas.weather import WeatherCreate, WeatherDTO
from app.uow.uow import UnitOfWork


class WeatherService:
    def __init__(self):
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def update_weather_for_city(self, city: str) -> WeatherDTO:
        current_user = SecurityContext.get_user()
        if not current_user:
            raise PermissionError("no, you can't watch weather without register/login")

        logger.info(f"request to open-meteo for {city}...")
        weather_data_input = self._fetch_from_meteo(city)

        with UnitOfWork() as uow:
            new_weather = WeatherData(
                location=weather_data_input.location,
                temperature=weather_data_input.temperature,
                humidity=weather_data_input.humidity,
                wind_speed=weather_data_input.wind_speed,
            )

            uow.weather.add(new_weather)
            uow.commit()

            logger.info("data succesfully saved to out database")

            return WeatherDTO.model_validate(new_weather)

    def get_weather_history(self, city: str) -> WeatherDTO:
        with UnitOfWork() as uow:
            weather = uow.weather.get_latest_by_city(city)
            if not weather:
                return None
            return WeatherDTO.model_validate(weather)

    def show_temperature_chart(self, city: str, days: int = 3):
        lat, lon, city_name = self._get_coordinates(city)
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m",
            "past_days": days,
            "forecast_days": 1,
        }

        responses = self.openmeteo.weather_api(
            settings.weather_api.WEATHER_URL, params=params
        )
        response = responses[0]

        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

        dates = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left",
        )

        df = pd.DataFrame({"time": dates, "temperature": hourly_temperature_2m})

        plt.figure(figsize=(10, 6))

        plt.plot(
            df["time"],
            df["temperature"],
            label="Temperature (°C)",
            color="orange",
            linewidth=2,
        )

        plt.title(f"Temperature dynamics: {city_name} (last {days} days)", fontsize=14)
        plt.xlabel("Time", fontsize=12)
        plt.ylabel("Temperature (°C)", fontsize=12)
        plt.grid(True, which="both", linestyle="--", alpha=0.7)
        plt.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        print("Done! Opening window...")
        plt.show()

    def _get_coordinates(self, city: str) -> tuple[float, float, str]:
        try:
            geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
            geo_resp = requests.get(settings.weather_api.GEO_URL, params=geo_params)
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                raise ValueError(f"City '{city}' is not found.")

            location = geo_data["results"][0]
            return location["latitude"], location["longitude"], location["name"]
        except requests.RequestException as e:
            raise ConnectionError(f"Error: {e}")

    def _fetch_from_meteo(self, city: str) -> WeatherCreate:
        try:
            geo_params = {"name": city, "count": 1, "language": "en", "format": "json"}
            geo_resp = requests.get(settings.weather_api.GEO_URL, params=geo_params)
            geo_data = geo_resp.json()

            if not geo_data.get("results"):
                raise ValueError(f"City '{city}' is not found.")

            location = geo_data["results"][0]
            lat = location["latitude"]
            lon = location["longitude"]
            city_name = location["name"]

            weather_params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            }
            weather_resp = requests.get(
                settings.weather_api.WEATHER_URL, params=weather_params
            )
            weather_data = weather_resp.json()

            current = weather_data.get("current", {})

            return WeatherCreate(
                location=city_name,
                temperature=current.get("temperature_2m"),
                humidity=current.get("relative_humidity_2m"),
                wind_speed=current.get("wind_speed_10m"),
            )

        except requests.RequestException as e:
            raise ConnectionError(f"error with API: {e}")
