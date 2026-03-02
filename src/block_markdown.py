from textnode import TextNode, TextType, TextDelimiter
from htmlnode import HTMLNode

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block:str)->BlockType:
    if block.startswith(tuple(["#"*i for i in range(1,7)])):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith(f"{block[0]}. ") and block[0].isnumeric():
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown:str)->list[str]:
    blocks = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks if b.strip() != ""]

    return blocks

def markdown_to_html(markdown:str)->HTMLNode:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = HTMLNode(block_type.value, block, )

    

# test = """# This is a heading

#       This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

# \n\n 


# - This is the first list item in a list block
# - This is a list item
# - This is another list item"""

# test = """
#     This is **bolded** paragraph

#     This is another paragraph with _italic_ text and `code` here
#     This is the same paragraph on a new line

#     - This is a list
#     - with items
#     """


# print(markdown_to_blocks(test))