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
