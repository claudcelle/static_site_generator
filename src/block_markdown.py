from textnode import TextNode, TextType, TextDelimiter
from htmlnode import HTMLNode,ParentNode,LeafNode,text_node_to_html_node
from inline_markdown import text_to_textnodes
import re

from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block:str)->BlockType:

    lines = block.split("\n")
    if block.startswith(tuple(["#"*i + " " for i in range(1,7)])):
        return BlockType.HEADING
    elif len(lines)>1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    # elif block.startswith(f"{block[0]}. ") and block[0].isnumeric():
    #     i = int(block[0])
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i+=1            
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown:str)->list[str]:
    blocks = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks if b.strip() != ""]

    return blocks

def text_to_children(text:str)->list[HTMLNode]:
    children = []
    textnodes = text_to_textnodes(text)
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    # children = [text_node_to_html_node(child) for child in children]
    return children



def count_hash_before_space(s):
    m = re.match(r"^#+(?=\s|$)", s)
    return len(m.group(0)) if m else 0

def block_to_nodes(block, block_type):
    
    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        content = ""
        for line in lines:
            content = " ".join([line.strip() for line in lines])
        return ParentNode("p", text_to_children(content))
    if block_type == BlockType.HEADING:
        tag = f"h{count_hash_before_space(block)}" 
        content = block.strip("#").strip()
        return ParentNode(tag, text_to_children(content))
    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        block_children = []
        for line in lines:
            inline_children = [] 
            content = line.strip("- ")
            inline_children = text_to_children(content)
            block_children.append(ParentNode("li", inline_children))
        block_node = ParentNode("ul", block_children)
        return block_node

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        block_children = []
        i = 1
        for line in lines:
            inline_children = [] 
            content = line.strip(f"{i}. ")
            i+=1
            inline_children = text_to_children(content)
            block_children.append(ParentNode("li", inline_children))
        block_node = ParentNode("ol", block_children)

        return block_node

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        children = []
        for line in lines:
            # print(line.strip(f"{i}. "))
            content = line.lstrip(f"> ")
            # children.append(LeafNode(None, content))
            children.extend(text_to_children(content))
        return ParentNode("blockquote",children)
    
    if block_type == BlockType.CODE:
        content = block.lstrip("```\n").rstrip("```")
        children = LeafNode("code",content)
        return ParentNode("pre", [children])

    return ParentNode("div", text_to_children(block))

def markdown_to_html_node(markdown:str)->HTMLNode:
    blocks = markdown_to_blocks(markdown) #spacchetta il testo in blocchi di testo separati da \n\n

    children = []


    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_nodes(block,block_type)
        print(node.to_html())
        children.append(node)
    main = ParentNode("div",children)

    return main