from abc import abstractmethod
from typing import Any, final, overload


class Language:
    @property
    def name(self) -> str:
        return self.__name

    @property
    def code(self) -> str:
        return self.__code

    def __init__(self, name: str, code: str):
        self.__name = name
        self.__code = code

    def __str__(self):
        return f"{self.name} ({self.code})"

    @abstractmethod
    def translate(self, text: str, exclude: list[str]) -> str:
        ...

    @overload
    def __call__(self, text: str) -> Any:
        ...

    @overload
    def __call__(self, text: str, exclude: list[str]) -> Any:
        ...

    @final
    def __call__(self, text: str, exclude: list[str] | None = None) -> Any:
        return self.translate(text, exclude or [])

    @final
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Language):
            return NotImplemented
        return self.name == value.name and self.code == value.code
