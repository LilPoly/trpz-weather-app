from typing import Optional

from app.schemas.user import UserDTO


class SecurityContext:
    _user: Optional[UserDTO] = None

    @classmethod
    def get_user(cls) -> Optional[UserDTO]:
        return cls._user

    @classmethod
    def set_user(cls, user: UserDTO):
        cls._user = user

    @classmethod
    def clear(cls):
        cls._user = None
