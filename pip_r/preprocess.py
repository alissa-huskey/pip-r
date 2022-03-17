from os import environ
from collections import defaultdict
from pathlib import Path

from parsimonious.nodes import NodeVisitor
from parsimonious.grammar import Grammar

"""
Environment variable names used by the utilities in the Shell and Utilities
volume of POSIX.1-2017 consist solely of uppercase letters, digits, and the
<underscore> ( '_' ) from the characters defined in Portable Character Set and
do not begin with a digit.

* https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap08.html
"""

spec = """
root                = (any env_var? any)*
env_var             =  var_open var_name var_close
any                 = ( ok_dollar / ~"[^$]*" )
ok_dollar           = "$" !"{"
var_open            = "${"
var_name            = ~"[A-Z_][A-Z0-9_]*"
var_close           = "}"
backslash           = "\57"
"""

grammar = Grammar(spec)

class EnvVar():
    """A class for the environment variables found when parsing."""
    def __init__(self, node):
        self.node = node
        self.name = node.text

    def __repr__(self):
        return f"EnvVar(name={self.name!r})"

    @property
    def value(self):
        """Return the value in the current environment."""
        return environ.get(self.name, "")

    @property
    def placeholder(self):
        """Return the placeholder text that will be replace."""
        return "${%s}" % self.name

    def replace(self, text):
        """Return text with placedholders replaced with values."""
        return text.replace(self.placeholder, self.value)

class Preprocessor(NodeVisitor):
    """A parsing class for preprocessing the requirements.txt file. (Just
    switching out environment variables.)"""

    def __init__(self, content):
        super().__init__()
        self.grammar = Grammar(spec)
        self.content = self.original = content
        self.vars = defaultdict(lambda: None)
        self.parsed = False

    def visit_root(self, node, visited_children):
        return self.vars

    def visit_var_name(self, node, visited_children):
        """Create an EnvVar object for each unique var_name found."""
        if not node.text:
            return

        self.vars[node.text] = self.vars[node.text] or EnvVar(node)

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return node or visited_children

    def parse(self):
        """Parse the saved content and turn on self.parsed"""
        self.parsed = True
        return super().parse(self.content)

    def process(self):
        """Replace all environment variables in self.content with their
           respective values."""
        if not self.parsed:
            raise Exception("You have to parse first!")

        for var in self.vars.values():
            self.content = var.replace(self.content)
        return self.content

def process_file(path):
    """Convenience function to parse and process a file."""
    path = Path(path)

    parser = Preprocessor(path.read_text())
    parser.parse()
    parser.process()
    return parser
