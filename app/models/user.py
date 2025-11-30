from sqlalchemy import Column, String

from app.enums.user import RoleEnum
from app.models.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default=RoleEnum.USER, index=True)
