"""
A simple example using the parsimonious parser

* https://github.com/erikrose/parsimonious
"""

from pprint import pprint

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor


grammar = Grammar(
"""
bold_text  = bold_open text bold_close
text       = ~"[A-Z 0-9]*"i
bold_open  = "(("
bold_close = "))"
""")


class Visitor(NodeVisitor):
    def visit_bold_text(self, node, visited_children):
        """Root level"""
        output = []
        for child in visited_children:
            #  breakpoint()
            output.append(child)
        return output

    def visit_bold_open(self, node, visited_children):
        return '\033[1m'

    def visit_bold_close(self, node, visited_children):
        return '\033[0m'

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return node.text


def main():
    tree = grammar.parse('((bold stuff))')
    visitor = Visitor()
    output = visitor.visit(tree)
    print("".join(output))

if __name__ == "__main__":
    main()
