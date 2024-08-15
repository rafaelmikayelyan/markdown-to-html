from htmlnode import LeafNode, ParentNode
from inline_to_textnode import *

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_bold_italic = "bold-italic"
text_type_strikethrough = "strikethrough"
text_type_highlight = "highlight"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__ (self, vs_node):
        return self.text == vs_node.text and self.text_type == vs_node.text_type and self.url == vs_node.url

    def __repr__ (self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

    def text_node_to_html_node(self):
        match self.text_type:
            case "text":
                return LeafNode(None, self.text)
            case "bold":
                return LeafNode("b", self.text)
            case "italic":
                return LeafNode("i", self.text)
            case "bold-italic":
                return ParentNode("b", [LeafNode("i", self.text)])
            case "strikethrough":
                return LeafNode("del", self.text)
            case "highlight":
                return LeafNode("mark", self.text)
            case "code":
                return LeafNode("code", self.text)
            case "link":
                return LeafNode("a", self.text, {"href": self.url})
            case "image":
                return LeafNode("img", "", {"src": self.url, "alt": self.text})
            case _:
                raise Exception(f"ERROR: {self.text_type}: text_type does not exist")
