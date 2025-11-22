from app.core.config.base import BaseConfig
from app.core.config.db import DbBaseConfig

__all__ = ["Settings", "settings"]


class Settings(BaseConfig):
    db: DbBaseConfig = DbBaseConfig()


settings = Settings()
