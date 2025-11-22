from pydantic import Field

from app.core.config.base import BaseConfig


class DbBaseConfig(BaseConfig):
    USER: str = Field(..., alias="POSTGRES_USER")
    PASSWORD: str = Field(..., alias="POSTGRES_PASSWORD")
    HOST: str = Field(..., alias="POSTGRES_HOST")
    PORT: str = Field(..., alias="POSTGRES_PORT")
    DB: str = Field(..., alias="POSTGRES_DB")

    @property
    def url(self) -> str:
        return f"postgresql+pg8000://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
