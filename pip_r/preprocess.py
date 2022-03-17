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

class Preprocessor(NodeVisitor):

    def __init__(self, content):
        super().__init__()
        self.grammar = Grammar(spec)
        self.content = content
        self.result = {}

    def visit_root(self, node, visited_children):
        return self.result

    def visit_var_name(self, node, visited_children):
        if not node.text:
            return

        self.result[node.text] = node

    def generic_visit(self, node, visited_children):
        """ The generic visit method. """
        return node or visited_children

    def parse(self):
        return super().parse(self.content)
