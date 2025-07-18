from typing import overload
from .Languages import Language
from .en import English


class Translator:
    def __init__(self):
        self.languages = {
            "en": English(),
        }

    def get_language(self, code: str) -> Language:
        return self.languages.get(code, self.languages["en"])

    @overload
    def translate(self, text: str, lang_code: str) -> str:
        ...

    @overload
    def translate(self, text: str, lang_code: str, exclude: list[str]) -> str:
        ...

    def translate(self, text: str, lang_code: str, exclude: list[str] | None = None) -> str:
        language = self.get_language(lang_code)
        if exclude is None:
            return language(text)
        return language(text, exclude)


__all__ = ["Translator"]
