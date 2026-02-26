import unittest
from textnode import TextNode, TextType, TextDelimiter
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
)
class TestSplitNodesDelimiter(unittest.TestCase):

    # You already have:
    # - test_split_nodes_code_valid
    # - test_split_nodes_code_open_delimiter

    # -------------------------
    # CODE (`) remaining cases
    # -------------------------

    def test_split_nodes_code_multiple_blocks(self):
        node = TextNode("a `b` c `d` e", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.PLAIN),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.PLAIN),
        ])

    def test_split_nodes_code_only_delimited(self):
        node = TextNode("`code`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [
            # TextNode("", TextType.PLAIN),
            TextNode("code", TextType.CODE),
            # TextNode("", TextType.PLAIN),
        ])

    def test_split_nodes_code_adjacent_blocks(self):
        node = TextNode("`a``b`", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [
            # TextNode("", TextType.PLAIN),
            TextNode("a", TextType.CODE),
            # TextNode("", TextType.PLAIN),
            TextNode("b", TextType.CODE),
            # TextNode("", TextType.PLAIN),
        ])

    def test_split_nodes_code_no_delimiter(self):
        node = TextNode("no code here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_code_empty_code(self):
        node = TextNode("a `` b", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            # TextNode("", TextType.CODE),
            TextNode(" b", TextType.PLAIN),
        ])

    # -------------------------
    # BOLD (**) cases
    # -------------------------

    def test_split_nodes_bold_valid(self):
        node = TextNode("This is **bold** text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.BOLD.value, TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
        ])

    def test_split_nodes_bold_multiple_blocks(self):
        node = TextNode("a **b** c **d** e", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.BOLD.value, TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.PLAIN),
            TextNode("d", TextType.BOLD),
            TextNode(" e", TextType.PLAIN),
        ])

    def test_split_nodes_bold_open_delimiter_raises(self):
        node = TextNode("a **bold text", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextDelimiter.BOLD.value, TextType.BOLD)

    def test_split_nodes_bold_close_delimiter_raises(self):
        node = TextNode("a bold** text", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextDelimiter.BOLD.value, TextType.BOLD)

    def test_split_nodes_bold_no_delimiter(self):
        node = TextNode("no bold here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.BOLD.value, TextType.BOLD)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_bold_empty_bold(self):
        node = TextNode("a **** b", TextType.PLAIN)  # empty bold segment between ****
        new_nodes = split_nodes_delimiter([node], TextDelimiter.BOLD.value, TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode(" b", TextType.PLAIN),
        ])

    # -------------------------
    # ITALIC (_) cases
    # -------------------------

    def test_split_nodes_italic_valid(self):
        node = TextNode("This is _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.ITALIC.value, TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.PLAIN),
        ])

    def test_split_nodes_italic_multiple_blocks(self):
        node = TextNode("a _b_ c _d_ e", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.ITALIC.value, TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.ITALIC),
            TextNode(" c ", TextType.PLAIN),
            TextNode("d", TextType.ITALIC),
            TextNode(" e", TextType.PLAIN),
        ])

    def test_split_nodes_italic_open_delimiter_raises(self):
        node = TextNode("a _italic text", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextDelimiter.ITALIC.value, TextType.ITALIC)

    def test_split_nodes_italic_close_delimiter_raises(self):
        node = TextNode("a italic_ text", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], TextDelimiter.ITALIC.value, TextType.ITALIC)

    def test_split_nodes_italic_no_delimiter(self):
        node = TextNode("no italic here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], TextDelimiter.ITALIC.value, TextType.ITALIC)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_italic_empty_italic(self):
        node = TextNode("a __ b", TextType.PLAIN)  # empty italic between __
        new_nodes = split_nodes_delimiter([node], TextDelimiter.ITALIC.value, TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode(" b", TextType.PLAIN),
        ])

    # -------------------------
    # NODE-LIST behavior cases
    # -------------------------

    def test_split_nodes_skips_non_plain_nodes(self):
        nodes = [
            TextNode("a `b` c", TextType.PLAIN),
            TextNode("already code", TextType.CODE),
        ]
        new_nodes = split_nodes_delimiter(nodes, TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.CODE),
            TextNode(" c", TextType.PLAIN),
            TextNode("already code", TextType.CODE),  # unchanged
        ])

    def test_split_nodes_processes_multiple_input_nodes(self):
        nodes = [
            TextNode("a `b`", TextType.PLAIN),
            TextNode(" c `d` e", TextType.PLAIN),
        ]
        new_nodes = split_nodes_delimiter(nodes, TextDelimiter.CODE.value, TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("a ", TextType.PLAIN),
            TextNode("b", TextType.CODE),
            # TextNode("", TextType.PLAIN),
            TextNode(" c ", TextType.PLAIN),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.PLAIN),
        ])

class TestExtractLinksAndImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertListEqual([("link", "https://www.google.com")], matches)
    
    def test_extract_mixed(self):
        text = "Ecco un link [alla home](https://boot.dev) e un'immagine ![di un orso](https://i.imgur.com/bear.png)"
        
        # Il link extractor NON deve prendere l'immagine
        links = extract_markdown_links(text)
        self.assertListEqual([("alla home", "https://boot.dev")], links)
        
        # L'image extractor NON deve prendere il link
        images = extract_markdown_images(text)
        self.assertListEqual([("di un orso", "https://i.imgur.com/bear.png")], images)
    def test_extract_empty(self):
        text = "Link vuoto []() e immagine vuota ![]()"

        links = extract_markdown_links(text)
        self.assertListEqual([("", "")], links)

        images = extract_markdown_images(text)
        self.assertListEqual([("", "")], images)
    def test_extract_multiple_consecutive(self):
        text = "[L1](U1)[L2](U2)![I1](IU1)![I2](IU2)"
        
        links = extract_markdown_links(text)
        self.assertListEqual([("L1", "U1"), ("L2", "U2")], links)
        
        images = extract_markdown_images(text)
        self.assertListEqual([("I1", "IU1"), ("I2", "IU2")], images)

    def test_extract_broken_markdown(self):
        # C'è uno spazio tra ! e [ -> non è un'immagine
        # C'è uno spazio tra ] e ( -> non è un link
        text = "Non un'immagine ! [alt](url) e non un link ! [link] (url)"
        
        links = extract_markdown_links(text)
        self.assertListEqual([], links)
        
        images = extract_markdown_images(text)
        self.assertListEqual([], images)

    def test_extract_complex_urls(self):
        text = "[Query](https://google.com/search?q=bootdev&src=regex) ![Image](https://site.com/img.png?size=large)"
        
        links = extract_markdown_links(text)
        self.assertListEqual([("Query", "https://google.com/search?q=bootdev&src=regex")], links)
        
        images = extract_markdown_images(text)
        self.assertListEqual([("Image", "https://site.com/img.png?size=large")], images)

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.PLAIN),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.PLAIN),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )



if __name__ == "__main__":
    unittest.main()
