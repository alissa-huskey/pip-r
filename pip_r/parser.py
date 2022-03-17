from functools import namedtuple
from pprint import pprint

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node

from pip_r.grammar import spec, walk


class Requirement:
    def __repr__(self):
        attrs = ", ".join([f"{k}={v!r}" for k, v in self.__dict__.items()])
        return f"Requirement({attrs})"
    pass

Attr = namedtuple("Attr", ["name", "value"])

class RequirementsFile(list):
    pass

class Parser(NodeVisitor):
    result = RequirementsFile()
    attrs = []

    def visit_root(self, node, visited_children):
        return self.result

    def visit_specification(self, node, visited_children):
        """
        The result is a tuple - name, list-of-extras,
        list-of-version-constraints-or-a-url, marker-ast or None
        """

        requirement = Requirement()

        for attr in self.attrs:
            setattr(requirement, *attr)

        self.result.append(requirement)
        self.attrs = []

        return requirement

    def visit_identifier(self, node, visited_children):
        attr = Attr("name", node.text)
        self.attrs.append(attr)
        return attr

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
