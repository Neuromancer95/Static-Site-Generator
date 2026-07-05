import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownBlocks(unittest.TestCase):



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
   
    def test_markdown_to_blocks_excessive_newlines(self):
        md ="""
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""  
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# Hello World"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```\nprint('Hello World')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    
    def test_unordered_list(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)  
    
    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)   
    
    def test_mixed_list(self):
        block = "- Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_missing_quote_symbol(self):
        block = "> This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_does_not_start_at_1(self):
        block = "2. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is a heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is a heading</h1></div>") 

    def test_unordered_list(self):
        md = """
- Item 1
- Item 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li></ul></div>") 
    
    def test_ordered_list(self):
        md = """
1. Item 1
2. Item 2
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Item 1</li><li>Item 2</li></ol></div>")    






if __name__ == "__main__":
    unittest.main() 