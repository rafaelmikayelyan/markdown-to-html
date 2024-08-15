import re

from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise ValueError("ERROR: Invalid markdown, formatted section not closed")
        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            if (i % 2) == 0:
                new_nodes.append(TextNode(split_nodes[i], text_type_text))
            else:
                new_nodes.append(TextNode(split_nodes[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("ERROR: Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        for link in links:
            split_nodes = node.text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_nodes) != 2:
                raise ValueError("ERROR: Invalid markdown, link section not closed")
            if split_nodes[0] != "":
                new_nodes.append(TextNode(split_nodes[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            node.text = split_nodes[1]
        if node.text != "":
            new_nodes.append(TextNode(node.text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    text_nodes = split_nodes_link([TextNode(text, text_type_text)])
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "***", text_type_bold_italic)
    text_nodes = split_nodes_delimiter(text_nodes, "**", text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, "*", text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, "`", text_type_code)
    text_nodes = split_nodes_delimiter(text_nodes, "~~", text_type_strikethrough)
    text_nodes = split_nodes_delimiter(text_nodes, "==", text_type_highlight)
    return text_nodes
