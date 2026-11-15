import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        delimiter_count = node.text.count(delimiter)
        if delimiter_count % 2 != 0:
            raise Exception(f"closing '{delimiter}' not found")
        count    = 1
        start_id = 0
        del_id   = 0
        if delimiter_count > 0:
            del_id   = node.text.index(delimiter)
        while count <= delimiter_count and delimiter_count != 0:
            if count % 2 == 0:
                new_nodes.append(TextNode(node.text[start_id:del_id], text_type))
            else:
                new_nodes.append(TextNode(node.text[start_id:del_id], TextType.TEXT))
            start_id = del_id + len(delimiter)
            count  = count + 1
            if delimiter not in node.text[start_id:]:
                break
            del_id = node.text.index(delimiter, start_id)
        if start_id != len(node.text):
            new_nodes.append(TextNode(node.text[start_id:], TextType.TEXT))

    return [n for n in new_nodes if n.text != ""]


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        start_id = 0
        end_id   = 0
        for alt, src in images:
            image  = f"![{alt}]({src})"
            end_id = node.text.index(image)
            new_nodes.append(TextNode(node.text[start_id:end_id], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, src))
            start_id = end_id + len(image)
        if start_id != len(node.text):
            new_nodes.append(TextNode(node.text[start_id:], TextType.TEXT))

    return [n for n in new_nodes if n.text != ""]


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        start_id = 0
        end_id   = 0
        for text, href in links:
            link  = f"[{text}]({href})"
            end_id = node.text.index(link)
            new_nodes.append(TextNode(node.text[start_id:end_id], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, href))
            start_id = end_id + len(link)
        if start_id >= len(node.text):
            new_nodes.append(TextNode(node.text[start_id:], TextType.TEXT))

    return [n for n in new_nodes if n.text != ""]


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '`',  TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '_',  TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
