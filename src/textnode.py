from enum import Enum


class TextType(Enum):
    PLAIN  = "plain"
    BOLD   = "bold"
    ITALIC = "italic"
    CODE   = "code"
    LINK   = "link"
    IMAGE  = "image"

class TextDelimiter(Enum):
    BOLD   = "**"
    ITALIC = "_"
    CODE   = "`"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url)

    def __repr__(self) -> str:
        string = ""
        for attr in self.__dict__:
            string += f"{attr!r}"
            string += "="
            string += f"{getattr(self,attr)!r}"
            string+=", "
        string = string.rstrip(', ')
        return f"{self.__class__.__name__}({string})"


