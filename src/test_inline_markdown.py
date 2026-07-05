
import unittest
from inline_markdown import extract_markdown_images, split_nodes_delimiter, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    

    def test_split_bold_delimiter(self):

        node = TextNode("before **middle** after", TextType.TEXT)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].text, "before ")
        self.assertEqual(result[0].text_type, TextType.TEXT)    

        self.assertEqual(result[1].text, "middle")
        self.assertEqual(result[1].text_type, TextType.BOLD)

        self.assertEqual(result[2].text, " after")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_code_delimiter(self):

        node = TextNode("before `middle` after", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].text, "before ")
        self.assertEqual(result[0].text_type, TextType.TEXT)    

        self.assertEqual(result[1].text, "middle")
        self.assertEqual(result[1].text_type, TextType.CODE)

        self.assertEqual(result[2].text, " after")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_split_italic_delimiter(self):

        node = TextNode("before _middle_ after", TextType.TEXT)

        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(len(result), 3)

        self.assertEqual(result[0].text, "before ")
        self.assertEqual(result[0].text_type, TextType.TEXT)    

        self.assertEqual(result[1].text, "middle")
        self.assertEqual(result[1].text_type, TextType.ITALIC)

        self.assertEqual(result[2].text, " after")
        self.assertEqual(result[2].text_type, TextType.TEXT)
   
    def test_unmatched_delimiter_raises(self):
        node = TextNode("before `middle after", TextType.TEXT)

        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_no_delimiter(self):
        node = TextNode("just normal text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "just normal text")
        self.assertEqual(result[0].text_type, TextType.TEXT)
    
    def test_preserve_non_text_nodes(self):
        node = TextNode("non-text node", TextType.BOLD)

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(len(result), 1)

        self.assertEqual(result[0].text, "non-text node")
        self.assertEqual(result[0].text_type, TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    
    def test_extract_markdown_links_with_image(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://example.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://example.com")], matches)
    
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
    def test_split_images_with_no_matches(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_images_match_at_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) is at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" is at the start", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_images_match_at_end(self):
        node = TextNode(
            "This is at the end ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is at the end ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    def test_split_images_non_text(self):
        node = TextNode(
            "This is a bold node",
            TextType.BOLD,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a bold node", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is another text with an ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("This is another text with an ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple_images_in_one_node(self):
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
    def test_split_links_no_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_split_links_at_start(self):
        node = TextNode(
            "[link](https://example.com) is at the beginning",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" is at the beginning", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_at_end(self):
        node = TextNode(
            "This is at the end [link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is at the end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )
    def test_split_links_multiple_nodes(self):
        node1 = TextNode(
            "This is text with a [link](https://example.com)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is another text with a [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode("This is another text with a ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://example.org"
                ),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **bold** and _italic_ and `code` and ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://example.com)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)
if __name__ == "__main__":
    unittest.main()

