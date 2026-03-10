import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html_node_headers(self):
        md = """# h1\n\n###### h6\n\n#not a header"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>h1</h1>", html)
        self.assertIn("<h6>h6</h6>", html)
        self.assertIn("<p>#not a header</p>", html)

    def test_markdown_to_html_node_lists(self):
        md = """- item 1\n- item 2\n\n1. first\n2. second"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<ul><li>item 1</li><li>item 2</li></ul>", html)
        self.assertIn("<ol><li>first</li><li>second</li></ol>", html)

    def test_markdown_to_html_node_code_and_quote(self):
        md = """```\ncode\n```\n\n> quote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<pre><code>code\n</code></pre>", html)
        self.assertIn("<blockquote>quote</blockquote>", html)

    def test_markdown_to_html_node_paragraphs(self):
        md = """This is a\nmulti-line paragraph.\n\nAnother one."""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<p>This is a multi-line paragraph.</p>", html)
        self.assertIn("<p>Another one.</p>", html)

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
        def test_markdown_to_blocks_newlines(self):
            md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                ],
            )
            
        def test_markdown_to_blocks_excessive_newlines(self):
            md = "a\n\n\n\nb"
            self.assertEqual(markdown_to_blocks(md), ["a", "b"])

        def test_markdown_to_blocks_leading_trailing_whitespace_per_block(self):
            md = "   a   \n\n\t  b\t"
            self.assertEqual(markdown_to_blocks(md), ["a", "b"])

        def test_markdown_to_blocks_preserves_internal_indentation(self):
            md = "line 1\n  indented line 2\n\nnext"
            self.assertEqual(
                markdown_to_blocks(md),
                ["line 1\n  indented line 2", "next"],
            )

        def test_markdown_to_blocks_only_whitespace_blocks_removed(self):
            md = "a\n\n   \n\nb"
            self.assertEqual(markdown_to_blocks(md), ["a", "b"])


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```\nThis is a code block\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is a list item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is a list item"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()

