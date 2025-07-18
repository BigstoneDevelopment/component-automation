from .Languages import Language


class English(Language):
    def __init__(self):
        super().__init__("English", "en")

    def translate(self, text: str, exclude: list[str]) -> str:
        # English is the default language, so we return the text as is
        return text
