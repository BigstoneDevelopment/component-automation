import enum
import re
from .color import Color
from typing import Literal


class IO(enum.Enum):
    I = "input".upper()  # noqa: E741
    O = "output".upper()  # noqa: E741
    B = "bidirectional".upper()  # noqa: E741


Direction = Literal["top", "bottom", "north", "south", "west", "east", "side"]


class Port():
    def __init__(self, type: IO, format: str, name: str, color: Color) -> None:
        self.type = type
        self.format = format.upper()
        self.name = name.upper()
        if not re.match(r"[IOB][A-Z]+(-[A-Z]+)?", self.name):
            self.name = f"""{self.type.name}{self.format}{
                "" if self.name == "ST" or self.name == "STANDARD" else f"-{self.name}"
                }"""
        self.color = color

    def __str__(self) -> str:
        return f"""{{text:\"{self.name}\",italic:true,color:\"{self.color}\"}}"""

    def __repr__(self) -> str:
        return str(self)


class Ports(list[Port]):
    def __str__(self) -> str:
        return "[" + ", {text:\", \",italic:true,color:\"dark_gray\"},".join(str(port) for port in self) + "]"

    def __repr__(self) -> str:
        return str(self)

    def direction_repr(self, direction: Direction) -> str:
        return f"[{{text:\"{direction.capitalize()}: \",italic:true,color:\"dark_gray\"}}," + repr(self)[1:]


__all__ = ["IO", "Port", "Ports", "Direction"]
