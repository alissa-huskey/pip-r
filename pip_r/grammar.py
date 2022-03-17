"""
Dependency Specification for Python Packages
* https://peps.python.org/pep-0508/#environment-m
"""

from parsimonious.grammar import Grammar


def walk(node, i=0):
    """Walk through a grammar tree"""
    if not i:
        #  yield i, node ; i += 1
        yield node ; i += 1
    for child in node.children:
        #  yield i, child ; i += 1
        yield child ; i += 1
        if child.children:
            yield from walk(child, i)

from collections import defaultdict

def groups(tree, show_all=False):
    """Returns a dictionary grouping grammar tree by:
       expr_name -> list(text...)
    """

    groups = defaultdict(list)

    for node in walk(tree):
        if show_all or not (node.expr_name and node.text):
            continue
        groups[node.expr_name].append(node.text)

    return groups

# TODO:
# [x] extras
# [ ] url
# [ ] path
# [ ] options
# [ ] global options
# [x] line continuation
# [ ] per-requirement options
# [ ] -f git+git://github.com/mozilla/elasticutils.git

spec = r"""
# ===================================================================================
# Syntax
# -----------------------------------------------------------------------------------
root                = white* line*

line                = wsp* ( specification / emptyline ) wsp* newline*

specification       = name wsp* extras? wsp* versionspec? wsp* marker? wsp* comment?

versionspec         = version_expr (wsp* "," version_expr)*
version_expr        = version_operator wsp* version
version             = wsp* ( alphanum / "-" / "_" / "." / "*" / "+" / "!" )+

marker              = semicolon wsp* marker_expr marker_multi*
marker_multi        = wsp+ ("and" / "or") wsp+ marker_expr
marker_expr         = "("* wsp* env_var wsp* marker_operator wsp* python_string wsp* ")"*

extras              = "[" wsp* identifier (wsp* "," wsp* identifier)* wsp* "]"

# ===================================================================================
# Tokens
# -----------------------------------------------------------------------------------

name                = &~"^[ \t]?"* identifier
identifier          = alphanum (alphanum / "-" / "_" / "." )* alphanum*
emptyline           = wsp* comment? white*
comment             = "# " not_newline
python_string       = (quote_double quotable_double+ quote_double)
                    / (quote_single quotable_single+ quote_single)

# ===================================================================================
# Word Lists
# -----------------------------------------------------------------------------------

marker_operator     = version_operator / (wsp* "in") / (wsp* "not" wsp+ "in")
version_operator    = wsp* ( "<=" / "<" / "!=" / "==" / ">=" / ">" / "~=" / "===" )

env_var             = ("python_version"                 / "python_full_version" /
                       "os_name"                        / "sys_platform"        /
                       "platform_release"               / "platform_system"     /
                       "platform_version"               / "platform_machine"    /
                       "platform_python_implementation" / "implementation_name" /
                       "implementation_version"         / "extra"               )

# ===================================================================================
# Character Groups
# -----------------------------------------------------------------------------------

alphanum            = ~"[a-zA-Z0-9]"
letter              = ~"[a-zA-Z]"
digit               = ~"[0-9]"

quotable_single     = ( (backslash quote_single) / not_quote_single )
quotable_double     = ( (backslash quote_double) / not_quote_double )

newline             = ~"[\n\r]*"
not_newline         = ~"[^\n\r]*"
white               = ~"[ \t\n\r]*"
wsp                 = ~"[ \t]*"

quote               = (quote_double / quote_single)

not_quote           = ~'[^\x27\x22]'
not_quote_double    = ~'[^\x22]'
not_quote_single    = ~'[^\x27]'


# ===================================================================================
# Individual Character Aliases
# -----------------------------------------------------------------------------------

backslash           = "\x5c"
quote_double        = "\x22"
quote_single        = "\x27"
semicolon           = "\x3b"

"""

if __name__ == "__main__":
    grammar = Grammar(spec)
