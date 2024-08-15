from htmlnode import *
from inline_to_textnode import *
from textnode import *

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered"
block_type_ordered_list = "ordered"

def markdown_to_blocks(markdown):
    return list(filter(None ,map(lambda x: x.strip(), markdown.split("\n\n"))))

def block_to_block_type(block):
    lines = block.split("\n")
    if (
            block.startswith("# ")
            or block.startswith("## ")
            or block.startswith("### ")
            or block.startswith("#### ")
            or block.startswith("##### ")
            or block.startswith("###### ")
        ):
        return block_type_heading
    elif lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    elif lines[0].startswith(">"):
        for i in range(len(lines) - 1):
            if not lines[i + 1].startswith(">"):
                return block_type_paragraph
        return block_type_quote
    elif lines[0].startswith("* ") or lines[0].startswith("- "):
        for i in range(len(lines) - 1):
            if not lines[i + 1].startswith("* ") and not lines[i + 1].startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    elif lines[0].startswith("1. "):
        for i in range(len(lines) - 1):
            if not lines[i + 1].startswith(f"{i + 2}. "):
                return block_type_paragraph
        return block_type_ordered_list
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(markdown_block_to_html_node(block))
    return ParentNode("div", children)

def markdown_block_to_html_node(block):
    if block_to_block_type(block) == block_type_paragraph:
        return markdown_paragraph_block_to_html_node(block)
    elif block_to_block_type(block) == block_type_code:
        return markdown_code_block_to_html_node(block)
    elif block_to_block_type(block) == block_type_quote:
        return markdown_quote_block_to_html_node(block)
    elif block_to_block_type(block) == block_type_heading:
        return markdown_heading_block_to_html_node(block)
    elif block_to_block_type(block) == block_type_unordered_list:
        return markdown_unordered_block_to_html_node(block)
    elif block_to_block_type(block) == block_type_ordered_list:
        return markdown_ordered_block_to_html_node(block)
    else:
        raise ValueError("ERROR: Invalid block type") 

def markdown_paragraph_block_to_html_node(block):
    paragraph = ""
    for line in block.split("\n"):
        paragraph += line + " "
    return ParentNode("p", markdown_line_to_html_node(paragraph.strip()))

def markdown_code_block_to_html_node(block):
    return ParentNode("pre", [ParentNode("code", markdown_line_to_html_node(block[4:-4]))])

def markdown_quote_block_to_html_node(block):
    quoteless_text = ""
    for line in block.split("\n"):
        quoteless_text += line[2:] + " "
    return ParentNode("blockquote", markdown_line_to_html_node(quoteless_text.strip()))

def markdown_heading_block_to_html_node(block):
    h_level = 0
    for i in range(7):
        if block[i:i+1] == "#":
            h_level = i + 1
        else:
            break
    return ParentNode(f"h{h_level}", markdown_line_to_html_node(block[h_level+1:]))

def markdown_unordered_block_to_html_node(block):
    html_nodes = []
    for line in block.split("\n"):
        html_nodes.append(ParentNode("li", markdown_line_to_html_node(line[2:])))
    return ParentNode("ul", html_nodes)

def markdown_ordered_block_to_html_node(block):
    html_nodes = []
    for line in block.split("\n"):
        html_nodes.append(ParentNode("li", markdown_line_to_html_node(line[3:])))
    return ParentNode("ol", html_nodes)

def markdown_line_to_html_node(line):
    text_nodes = text_to_textnodes(line)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(node.text_node_to_html_node())
    return html_nodes

def extract_title(markdown):
    if markdown.startswith("# "):
        return markdown.split("\n")[0][2:].strip()
    else:
        raise Exception("ATTENTION! No title found")
