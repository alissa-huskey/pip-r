from functools import namedtuple, partialmethod
from pprint import pprint

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node

from pip_r.grammar import spec, walk


class Requirement:
    name, extras, versionspec, URI, markers, comment = [""] * 6

    def __repr__(self):
        attrs = ", ".join([f"{k}={v!r}" for k, v in self.__dict__.items()])
        return f"Requirement({attrs})"
    pass

Attr = namedtuple("Attr", ["name", "value"])

class RequirementsFile(list):
    pass

class Parser(NodeVisitor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = RequirementsFile()
        self.attrs = []

    def visit_root(self, node, visited_children):
        return self.result

    def visit_specification(self, node, visited_children):
        """
        The result is a tuple - name, list-of-extras,
        list-of-version-constraints-or-a-url, marker-ast or None
        """

        if not node.text:
            return

        requirement = Requirement()

        for attr in self.attrs:
            setattr(requirement, *attr)

        self.result.append(requirement)
        self.attrs = []

        return requirement

    def attr_visitor(self, name, node, visited_children):
        attr = Attr(name, node.text)
        self.attrs.append(attr)
        return attr

    visit_name = partialmethod(attr_visitor, "name")
    visit_extras = partialmethod(attr_visitor, "extras")
    visit_versionspec = partialmethod(attr_visitor, "versionspec")
    visit_URI = partialmethod(attr_visitor, "URI")
    visit_marker = partialmethod(attr_visitor, "marker")
    visit_comment = partialmethod(attr_visitor, "comment")

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return node or visited_children


def main():
    tree = grammar.parse("""
pynvim
more-itertools
""")

    #  print(tree.prettily())

    parser = Parser()
    output = parser.visit(tree)
    pprint(output)

if __name__ == "__main__":
    main()
