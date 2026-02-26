import re
from textnode import TextNode,TextType, TextDelimiter

def extract_markdown_images(text):
    pattern = r"(?<!\! )\!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
     
def extract_markdown_links(text):
    pattern = r"(?<!!)(?<!\! )\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN: 
            new_nodes.append(node)
            continue
        split_nodes = []
        buff = node.text.split(sep=delimiter)    
        # if node.text.count(delimiter) % 2 != 0:
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
        # print(buff)
    # pprint(new_nodes)
    return new_nodes


def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        assert node.text_type == TextType.PLAIN, "only plain text supported"
        
        pattern = r"((?:.*?))\[(.*?)\]\((.*?)\)"

        ziplist = re.findall(pattern, node.text)
        for item in ziplist:
            # print(item)
            result.append(TextNode(item[0], TextType.PLAIN))
            result.append(TextNode(item[1], TextType.LINK, item[2]))
            # result.append(TextNode(item[3], TextType.PLAIN))

    return result

    
def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        assert node.text_type == TextType.PLAIN, "only plain text supported"
        
        pattern = r"((?:.*?))!\[(.*?)\]\((.*?)\)"
        ziplist = re.findall(pattern, node.text)
        for item in ziplist:
            # print(item)
            result.append(TextNode(item[0], TextType.PLAIN))
            result.append(TextNode(item[1], TextType.IMAGE, item[2]))
            # result.append(TextNode(item[3], TextType.PLAIN))

    return result

