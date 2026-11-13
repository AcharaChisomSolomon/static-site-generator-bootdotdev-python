class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None,
            value: str | None = None,
            children: list["HTMLNode"] | None = None, 
            props: dict[str, str] | None = None, 
        ):
        self.tag      = tag
        self.value    = value
        self.children = children
        self.props    = props

    def to_html(self):
        raise NotImplementedError("to be implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join([f' {key}="{self.props[key]}"' for key in self.props])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("node must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is required")
        if self.children is None:
            raise ValueError("children are required")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()
        return f"<{self.tag}>{html_string}</{self.tag}>"
