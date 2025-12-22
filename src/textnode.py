from enum import Enum

class TextType(Enum):
        PLAIN  = "plain"
        BOLD   = "bold"
        ITALIC = "italic"
        CODE   = "code"
        LINK   = "link"
        IMAGE  = "image"

class TextNode:
    def __init__(self,text:str, text_type:TextType, url: str|None=None) -> None:
        
        self.text = text
        self.text_type = text_type
        self.url = url 

    def __eq__(self, value: object) -> bool:
         
        if isinstance(value, TextNode):
              
            eq = True
            for attr in self.__dict__:
                eq *= getattr(self,attr) == getattr(value,attr)
            return bool(eq)
            
        return False

    def __repr__(self) -> str:
        string = ""
        for attr in self.__dict__:
            string += f"{attr!r}"
            string += "="
            string += f"{getattr(self,attr)!r}"
            string+=", "
        string = string.rstrip(', ')
        return f"{self.__class__.__name__}({string})"


# a = TextNode("aaa",TextType.PLAIN)
# # b = TextNode("aba",TextType.PLAIN,"www.culo.it")

# print(a)

# print(a == b)

