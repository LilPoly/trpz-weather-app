from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., description="User's name")
    email: EmailStr = Field(..., description="User's email")


class UserCreate(UserBase):
    password: str = Field(..., min_length=4, description="User's password")


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(..., min_length=4, description="User's password")


class UserDTO(UserBase):
    id: int = Field(..., description="User's id")
    role: str = Field(..., description="User's role. Can be USER or ADMIN")

    model_config = ConfigDict(from_attributes=True)
