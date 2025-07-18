
from collections import defaultdict
import re
import time
from typing import Literal, Self
import os

from translator import Translator


AllValidComponentsTemplate = Literal[
    "structure_file_name",
    "structure_display_name",
    "structure_author",
    "structure_description",
    "ports",
    "namespace",
    "model"
]


class Template:
    __finished: dict[str, bool] = defaultdict(lambda: False)

    def __init__(self, content: str) -> None:
        content = content.strip()
        self.append = content.startswith("APPEND:")
        if self.append:
            content = content.removeprefix("APPEND:").strip()
        self.PATH = content.splitlines()[0].strip().removeprefix("PATH:").strip()
        self.content = "\n".join(content.splitlines()[1:])
        self.prereplace()

    def prereplace(self) -> None:
        self.content = re.sub(r"<time>", lambda _: f"<{time.asctime()}>", self.content)

    def replace(self, **kwargs: str | list[str]) -> Self:
        if not kwargs:
            return self
        repeats: list[tuple[str, str, str]] = re.findall(r"<repeat \"(\w*?) in (.*?)\" \"(.*?)\">", self.content, re.DOTALL)
        while repeats:
            for repeat_key, repeater, repeat_value in repeats:
                try:
                    iterable = eval(repeater, {}, kwargs)
                except Exception as e:
                    raise ValueError(f"Failed to evaluate repeater: {repeater}") from e

                output = ""
                for item in iterable:
                    formatted = repeat_value.replace(f"{{{repeat_key}}}", str(item))
                    output += formatted

                self.content = self.content.replace(f'<repeat "{repeat_key} in {repeater}" "{repeat_value}">', output)

            repeats = re.findall(r"<repeat \"(\w*?) in (.*?)\" \"(.*?)\">", self.content, re.DOTALL)
        result = self.content
        for key, value in kwargs.items():
            result = result.replace(f"<{key}>", value if isinstance(value, str) else ",".join(value))
            if isinstance(value, list):
                for i in range(len(value)):
                    result = result.replace(f"<{key}[{i}]>", value[i])
        self.content = result
        return self

    def postreplace(self, lang_code: str) -> Self:
        self.content = Translator().translate(self.content, lang_code)
        return self

    def finished(self, lang_code: str = "en") -> bool:
        if self.__finished[lang_code]:
            return True
        self.postreplace(lang_code)
        self.__finished[lang_code] = True
        return not re.search(r"<.*>", self.content, re.DOTALL)

    def save(self) -> None:
        with open(self.PATH, "a" if self.append else "w") as file:
            file.write(self.content + "\n")


TEMPLATES: dict[str, Template] = {}

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
if os.path.exists(templates_dir) and os.path.isdir(templates_dir):
    for filename in os.listdir(templates_dir):
        file_path = os.path.join(templates_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding='utf-8') as template_file:
                content = template_file.read()
                TEMPLATES[filename] = Template(content)


__all__ = ["Template", "TEMPLATES", "AllValidComponentsTemplate"]
