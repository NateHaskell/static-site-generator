import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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
        
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")  
    
    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")  

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")  

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me") 
        self.assertEqual(html_node.props["href"], "https://example.com") 
    
    def test_image(self):
        node = TextNode("alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "") 
        self.assertEqual(html_node.props["src"], "https://example.com/image.png") 
        self.assertEqual(html_node.props["alt"], "alt text") 
    
    def test_invalid_text_type(self):
        # Create a mock TextType that isn't one of the valid ones
        # This requires a bit of setup to create an invalid text_type
        from unittest.mock import Mock
        mock_text_type = Mock()
        mock_text_type.name = "INVALID"
        node = TextNode("Some text", mock_text_type)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    

if __name__ == "__main__":
    unittest.main()