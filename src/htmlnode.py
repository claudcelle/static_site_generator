from typing import List, Dict, Optional


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

    # def __repr__(self) -> str:
    #     return (
    #         f"HTMLNode(tag={self.tag!r}, "
    #         f"value={self.value!r}, "
    #         # f"children={len(self.children) if self.children else 0}, "
    #         f"children={self.children}, "
    #         f"props={self.props!r})"
    #     )
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"



class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str,  props: Optional[Dict[str, object]] | None = None) -> None:
        """
        Initializes a LeafNode object.

        Args:
            tag (str | None): The tag of the node. Not optional (no default), can be None though
            value (str): The value of the node.
            props (Optional[Dict[str, object]] | None, optional): The props of the node. Defaults to None.

        Raises:
            ValueError: If the value is None.
        """
        
        super().__init__(tag=tag, value=value,children = None, props=props)
    
    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode requires not-None value")
        if not self.tag:
            return f'{self.value}'
        if self.props:
            return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
        

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Optional[Dict[str, object]] | None = None) -> None:
        super().__init__(tag=tag, value = None, children = children, props = props)

    def to_html(self) -> str | None:
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError(f"Missing children nodes: {self.__qualname__} requires children node")
        self.value = ""
        for child in self.children:
            self.value += child.to_html()
            # res += '\n'
        # return res
        if self.props:
            return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'

        
        
# print((LeafNode(tag = 'a', value = 'value',props={"href": "https://www.google.com"}).to_html()))

# node = ParentNode(
#     "p",
#     [
#         LeafNode("b", "Bold text"),
#         LeafNode(None, "Normal text"),
#         LeafNode("i", "italic text"),
#         LeafNode(None, "Normal text"),
#     ],
# )
# print(node.to_html())
