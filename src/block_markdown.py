from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block:str) -> BlockType:

    lines = block.split("\n")
    if block.startswith(tuple(["#" * i + " " for i in range(1, 7)])):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
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
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [b.strip() for b in blocks if b.strip() != ""]
    return blocks


def text_to_children(text: str) -> list[HTMLNode]:
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in textnodes]


def count_hash_before_space(s: str) -> int:
    m = re.match(r"^#+(?=\s|$)", s)
    return len(m.group(0)) if m else 0


def block_to_nodes(block: str, block_type: BlockType) -> HTMLNode:
    
    if block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        content = " ".join(line.strip() for line in lines)
        return ParentNode("p", text_to_children(content))

    if block_type == BlockType.HEADING:
        tag = f"h{count_hash_before_space(block)}"
        content = block.strip("#").strip()
        return ParentNode(tag, text_to_children(content))

    if block_type == BlockType.UNORDERED_LIST:
        lines = block.split("\n")
        items = []
        for line in lines:
            content = line[2:]
            items.append(ParentNode("li", text_to_children(content)))
        return ParentNode("ul", items)

    if block_type == BlockType.ORDERED_LIST:
        lines = block.split("\n")
        items = []
        i = 1
        for line in lines:
            prefix = f"{i}. "
            content = line[len(prefix) :]
            items.append(ParentNode("li", text_to_children(content)))
            i += 1
        return ParentNode("ol", items)

    if block_type == BlockType.QUOTE:
        lines = block.split("\n")
        content = " ".join(line[2:] for line in lines)
        return ParentNode("blockquote", text_to_children(content))

    if block_type == BlockType.CODE:
        lines = block.split("\n")
        content = "\n".join(lines[1:-1])
        if len(lines) > 2:
            content += "\n"
        child = LeafNode("code", content)
        return ParentNode("pre", [child])

    return ParentNode("div", text_to_children(block))


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_nodes(block, block_type))
    return ParentNode("div", children)
