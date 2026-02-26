import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_check_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        return node.url is None


# class TestSplitNodesDelimiter(unittest.TestCase):
#     def test_split_nodes_code_valid(self):
#         node = TextNode("This is text with a `code block` word", TextType.PLAIN)
#         new_nodes = split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)
#         self.assertEqual(new_nodes, [
#             TextNode("This is text with a ", TextType.PLAIN), 
#             TextNode("code block", TextType.CODE), 
#             TextNode(" word", TextType.PLAIN),])
#     def test_split_nodes_code_open_delimiter(self):
#         node = TextNode("This is text with a code block` word with non closed delimiter", TextType.PLAIN)
#         with self.assertRaises(Exception):            
#             split_nodes_delimiter([node], TextDelimiter.CODE.value, TextType.CODE)



if __name__ == "__main__":
    unittest.main()
