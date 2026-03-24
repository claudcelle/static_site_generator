from typing import Dict, List, Optional

from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HTMLNode"]] = None,
        props: Optional[Dict[str, object]] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str|None:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        """
        Ritorna una stringa del tipo:
        ' href="https://www.google.com" target="_blank"'
        oppure '' se non ci sono props.
        """
        if not self.props:
            return ""

        string = ""
        for key, val in self.props.items():
            string += f' {key}="{val}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """
        Initializes a LeafNode object.

        Args:
            tag (str | None): The tag of the node. Not optional (no default), can be None though
            value (str): The value of the node.
            props (Optional[Dict[str, object]] | None, optional): The props of the node. Defaults to None.

        Raises:
            ValueError: If the value is None.
        """
        
    def __init__(
        self, tag: str | None, value: str, props: Optional[Dict[str, object]] | None = None
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode requires not-None value")
        if not self.tag:
            return f"{self.value}"
        if self.props:
            return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"
        return f"<{self.tag}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: List[HTMLNode],
        props: Optional[Dict[str, object]] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str | None:
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError(f"{self.__qualname__} requires at least one child")

        rendered = "".join(child.to_html() for child in self.children)
        if self.props:
            return f"<{self.tag}{super().props_to_html()}>{rendered}</{self.tag}>"
        return f"<{self.tag}>{rendered}</{self.tag}>"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(tag = None,
                            value = text_node.text)
        case TextType.BOLD:
            return LeafNode(tag = "b",
                            value = text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag = "i",
                            value = text_node.text)
        case TextType.CODE:
            return LeafNode(tag = "code",
                            value = text_node.text)
        case TextType.LINK:
            return LeafNode(tag = "a",
                            value = text_node.text,
                            props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text},
            )
