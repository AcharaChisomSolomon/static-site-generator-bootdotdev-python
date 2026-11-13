import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_to_html_with_properties(self):
        node = HTMLNode(tag="p", value="hello", props={
            "href": "https://www.google.com", 
            "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"'
        )

    def test_prop_to_html_without_properties(self):
        node = HTMLNode(tag="p", value="hello")
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
