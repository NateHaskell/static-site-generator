import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url=None)
        self.assertEqual(node, node2)
    
    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, url="https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, url="https://www.boot.dev")
        self.assertEqual(node, node2)
    
    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("Different text", TextType.BOLD, url=None)
        self.assertNotEqual(node, node2)
    
    def test_eq_text_empty(self):
        node = TextNode("", TextType.BOLD, url=None)
        node2 = TextNode("", TextType.BOLD, url=None)
        self.assertEqual(node, node2)
    
    def test_not_eq_text_empty(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("", TextType.BOLD, url=None)
        self.assertNotEqual(node, node2)
    
    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


    

if __name__ == "__main__":
    unittest.main()