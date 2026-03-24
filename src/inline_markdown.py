import re

from textnode import TextDelimiter, TextNode, TextType

_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")
_LINK_RE = re.compile(r"(?<!!)(?<!\! )\[([^\]]*)\]\(([^)]*)\)")


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return _IMAGE_RE.findall(text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return _LINK_RE.findall(text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        split_nodes = []
        buff = node.text.split(sep=delimiter)
        if len(buff) % 2 == 0:
            raise ValueError(f"Delimiter {delimiter} not matched; Invalid Markdown syntax")
        for i in range(len(buff)):
            if buff[i] == "":
                continue
            if i % 2 == 1:
                split_nodes.append(TextNode(buff[i], text_type))
            else:
                split_nodes.append(TextNode(buff[i], TextType.PLAIN))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            result.append(node)
            continue
        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError(f"Delimiter {link[0]} not matched; Invalid Markdown syntax")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]
        if text != "":
            result.append(TextNode(text, TextType.PLAIN))
    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            result.append(node)
            continue
        for image_alt, image_link in images:
            sections = text.split(f"![{image_alt}]({image_link})", maxsplit=1)
            if len(sections) != 2:
                raise ValueError(
                    f"Delimiter {image_alt} not matched; Invalid Markdown syntax"
                )
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.PLAIN))
            result.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]
        if text != "":
            result.append(TextNode(text, TextType.PLAIN))
    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    texttype_to_delimiter = {
        TextType.BOLD: TextDelimiter.BOLD,
        TextType.ITALIC: TextDelimiter.ITALIC,
        TextType.CODE: TextDelimiter.CODE,
    }
    node = TextNode(text, TextType.PLAIN)
    results = split_nodes_image([node])
    results = split_nodes_link(results)
    for text_type, delimiter in texttype_to_delimiter.items():
        results = split_nodes_delimiter(results, delimiter.value, text_type)
    return results
