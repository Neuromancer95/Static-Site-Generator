from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            sections = node.text.split(delimiter) 
            
            if len(sections) == 1:
                new_nodes.append(node)
            elif len(sections) % 2 == 0:
                raise Exception("unmatched pair")
            else:
                for i, section in enumerate(sections):
                    if section == "":
                        continue    
                    if i % 2 == 0:
                        new_nodes.append(TextNode(section, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(section, text_type))
        else:
                    new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    
    pattern_images = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern_images, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
             new_nodes.append(node)
             continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for image in images:
            image_alt, image_url = image
            sections = remaining_text.split(f"![{image_alt}]({image_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes
    
def split_nodes_link(old_nodes):
    new_nodes = []
        
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for link in links:
            link_text, link_url = link
            sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            remaining_text = sections[1]
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
           
    return nodes
         
