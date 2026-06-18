import unittest
from copystatic import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_extract_simple_h1(self):
        markdown = "# Titolo"
        self.assertEqual(extract_title(markdown), "Titolo")

    def test_extract_h1_with_spaces(self):
        markdown = "#   Titolo con spazi   "
        self.assertEqual(extract_title(markdown), "Titolo con spazi")

    def test_extract_first_header(self):
        markdown = "testo iniziale\n# Titolo\naltro testo"
        self.assertEqual(extract_title(markdown), "Titolo")

    def test_extract_header_with_multiple_hashes(self):
        markdown = "### Sottotitolo"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No h1 header")

    def test_empty_markdown_raises_exception(self):
        with self.assertRaises(Exception) as context:
            extract_title("")

        self.assertEqual(str(context.exception), "Markdown is empty")

    def test_none_markdown_raises_exception(self):
        with self.assertRaises(Exception) as context:
            extract_title(None)

        self.assertEqual(str(context.exception), "Markdown is empty")

    def test_non_string_markdown_raises_type_error(self):
        with self.assertRaises(TypeError) as context:
            extract_title(123)

        self.assertEqual(str(context.exception), "Content must be text")

    def test_no_header_raises_exception(self):
        markdown = "Questo testo non contiene header"
        with self.assertRaises(Exception) as context:
            extract_title(markdown)

        self.assertEqual(str(context.exception), "No h1 header")


if __name__ == "__main__":
    unittest.main()