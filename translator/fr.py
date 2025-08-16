from deep_translator import GoogleTranslator
from .Languages import Language


class French(Language):
    def __init__(self):
        super().__init__("French", "fr")

    def translate(self, text: str, exclude: list[str]) -> str:
        # Google Translate is pretty accurate for French (ChatGPT is still better)
        excluded = []
        parsed_text = ""
        while text:
            if any([text.startswith(item) for item in exclude]):
                for item in exclude:
                    if text.startswith(item):
                        excluded.append(item)
                        text = text[len(item):]
                        parsed_text += "[REDACTED]"
                        break
            else:
                parsed_text += text[0]
                text = text[1:]
        translated_parsed_text = GoogleTranslator(source="en", target="fr").translate(parsed_text)
        index = 0
        while "[REDACTED]" in translated_parsed_text:
            translated_parsed_text = translated_parsed_text.replace("[REDACTED]", f"{excluded[index]}", 1)
            index += 1
        return translated_parsed_text
