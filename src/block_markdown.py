from textnode import TextNode, TextType, TextDelimiter

def markdown_to_blocks(markdown:str)->list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    for idx,line in enumerate(blocks):
        strl = line.split("\n")
        blocks[idx] = "\n".join(list(map(lambda x: x.strip(), strl)))
    blocks= [block for block in blocks if block!=""]

    return blocks


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