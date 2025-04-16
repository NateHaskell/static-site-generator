import unittest
import re
from markdown import  (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link, 
    text_to_textnodes,
    extract_markdown_images, 
    extract_markdown_links
)
from textnode import TextType, TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code_block(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        TextNode("This is text with a **bold** word", TextType.TEXT),
        TextNode("This is text with an _italic_ word", TextType.TEXT)
    ])
    
    def test_split_nodes_delimiter_bold(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
        TextNode("This is text with an _italic_ word", TextType.TEXT)
    ])
        
    def test_split_nodes_delimiter_italic(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("This is text with a **bold** word", TextType.TEXT),
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
    ])
    
    def test_split_nodes_delimiter_invalid_markdown(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with an _italic word", TextType.TEXT)
        old_nodes = [node1, node2, node3]
        
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)

    def test_split_nodes_delimiter_multiple_occurences(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("This is text with a **bold** word", TextType.TEXT)
        node3 = TextNode("This is text with two _italic_ words _in_ it", TextType.TEXT)
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        TextNode("This is text with a **bold** word", TextType.TEXT),
        TextNode("This is text with two ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" words ", TextType.TEXT),
        TextNode("in", TextType.ITALIC),
        TextNode(" it", TextType.TEXT),
    ])

    def test_split_nodes_delimiter_with_mixed_types(self):
        node1 = TextNode("Regular text", TextType.TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("Text with `code`", TextType.TEXT)
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
    
        self.assertEqual(new_nodes, [
        TextNode("Regular text", TextType.TEXT),
        TextNode("Already bold", TextType.BOLD),  # This should remain unchanged
        TextNode("Text with ", TextType.TEXT),
        TextNode("code", TextType.CODE),
    ])    

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
    )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )
    
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )
    

if __name__ == "__main__":
    unittest.main()