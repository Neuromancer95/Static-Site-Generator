from enum import Enum
from htmlnode import ParentNode
from inline_markdown import  text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown: str) -> list[str]:

    parts = markdown.split("\n\n")
    blocks = []
    for part in parts:
        stripped = part.strip()
        if stripped:
            blocks.append(stripped)
    return blocks


    
def block_to_block_type(block: str) -> BlockType:
    stripped = block.strip()
    if stripped.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    lines = block.split("\n")
    if lines[0].startswith("```") and lines[-1].startswith("```") and len(lines) > 1:
        return BlockType.CODE
    if stripped.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if stripped.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if stripped.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
        


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)

def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_block_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_block_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_block_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_block_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_block_to_html_node(block)
    elif block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_block_to_html_node(block):
    count = 0
    for i in range(len(block)):
        if block[i] == "#":
            count += 1
        else:
            break
    text = block[count + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)

def code_block_to_html_node(block):
    stripped = block[4:-3]
    raw_text_node = TextNode(stripped, TextType.TEXT)
    return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(raw_text_node)])])

def quote_block_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        stripped = line[1:].strip()
        new_lines.append(stripped)
    text = "\n".join(new_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        stripped = line[2:].strip()
        li_children = text_to_children(stripped)
        children.append(ParentNode("li", li_children))
    return ParentNode("ul", children)

def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        stripped = line[line.index(".") + 1 :].strip()
        li_children = text_to_children(stripped)
        children.append(ParentNode("li", li_children))
    return ParentNode("ol", children)
