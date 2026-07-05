import unittest
from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_props(self):
        node = HTMLNode(
            "a",
            "Boot.dev",
            None,
            {"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.boot.dev" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")

    def test_htmlnode_repr(self):
        node = HTMLNode("p", "hello", None, {"class": "text"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=p, value=hello, children=None, props={'class': 'text'})"
        )

    def test_to_html_raises(self):
        node = HTMLNode("p", "hello")
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_with_tag(self):
        node = LeafNode("p", "hello")
        self.assertEqual(node.to_html(), "<p>hello</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "hello")
        self.assertEqual(node.to_html(), "hello")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Boot.dev", {"href": "https://www.boot.dev"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev">Boot.dev</a>'
        )


class TestParentNode(unittest.TestCase):
    # Basic single child
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

# Nested ParentNode (grandchildren)
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

# Multiple children of mixed types
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
     )

# Props on the parent node
    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>child</span></div>',
        )

# Raise ValueError when no tag
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

# Different parent tags (e.g. headings)
    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text</h2>",
        )


if __name__ == "__main__":
    unittest.main()