from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.config import settings
from app.models.base import BaseModel

engine = create_engine(settings.db.url)

SessionFactory = sessionmaker(autoflush=True, bind=engine)


def create_db():
    BaseModel.metadata.create_all(bind=engine)
