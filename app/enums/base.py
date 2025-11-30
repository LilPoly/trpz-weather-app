from enum import StrEnum


class BaseStrEnum(StrEnum):
    @classmethod
    def list(cls) -> list[str]:
        return list(cls.__members__.values())
