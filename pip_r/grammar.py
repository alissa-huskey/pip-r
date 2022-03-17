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
# [ ] environment variables

spec = r"""
# ===================================================================================
# Syntax
# -----------------------------------------------------------------------------------
root                = white* line*

line                = wsp* ( specification / emptyline ) wsp* newline*

# name_req      = (name wsp* extras? wsp* versionspec? wsp* quoted_marker?
# url_req       = (name wsp* extras? wsp* urlspec (wsp+ | end) quoted_marker?
specification       = name wsp* extras? wsp* ((versionspec wsp*) / (urlspec (wsp+ / newline)))? marker? wsp* comment?

versionspec         = version_expr (wsp* "," version_expr)*
version_expr        = version_operator wsp* version
version             = wsp* ( alphanum / "-" / "_" / "." / "*" / "+" / "!" )+

marker              = semicolon wsp* marker_expr marker_multi*
marker_multi        = wsp+ ("and" / "or") wsp+ marker_expr
marker_expr         = "("* wsp* env_var wsp* marker_operator wsp* python_string wsp* ")"*

extras              = "[" wsp* identifier (wsp* "," wsp* identifier)* wsp* "]"

urlspec             = "@" wsp* URI

# ===================================================================================
# Tokens
# -----------------------------------------------------------------------------------

name                = &~"^[ \t]?"* identifier
identifier          = alphanum (alphanum / "-" / "_" / "." )* alphanum*
emptyline           = wsp* comment? white*
comment             = "# " not_newline
python_string       = (quote_double quotable_double+ quote_double)
                    / (quote_single quotable_single+ quote_single)

URI                 = (scheme ":")? hier_part ("?" fragment )? ( "#" fragment)?
scheme              = letter ( letter / digit / "+" / "-" / ".")*
hier_part           = ('//' authority path_abempty) / path_absolute / path_rootless # / path_empty

path_abempty        =  ( '/' segment)*                         # begins with '/' or is empty
path_absolute       =  '/' ( segment_nz ( '/' segment)* )?     # begins with '/' but not '//'
path_noscheme       =  segment_nz_nc ( '/' segment)*           # begins with a non-colon segment
path_rootless       = segment_nz ( '/' segment)*               # begins with a segment
path_empty          = ""                                       # zero characters

authority           = ( userinfo "@" )? host ( ":" port )?
userinfo            = ( unreserved / pct_encoded / sub_delims / ":")*
host                = IP_literal / IPv4address / reg_name
port                = digit*
reg_name            = ( unreserved / pct_encoded / sub_delims)*
pct_encoded         = "%" hexdig

IP_literal          = "[" ( IPv6address / IPvFuture) "]"
IPvFuture           = "v" hexdig+ "." ( unreserved / sub_delims / ":")+
IPv4address         = dec_octet "." dec_octet "." dec_octet "." dec_octet
IPv6address         = ((                                                                    h16c h16c h16c h16c h16c h16c ls32 ) /
                       (                                                               "::" h16c h16c h16c h16c h16c h16c ls32 ) /
                       (                                                  h16        ? "::" h16c h16c h16c h16c           ls32 ) /
                       (                                    (h16c? (h16c? h16      ))? "::" h16c h16c h16c                ls32 ) /
                       (                             (h16c? (h16c? (h16c? h16     )))? "::" h16c h16c                     ls32 ) /
                       (                      (h16c? (h16c? (h16c? (h16c? h16    ))))? "::" h16 ":"                       ls32 ) /
                       (               (h16c? (h16c? (h16c? (h16c? (h16c? h16   )))))? "::" ls32                               ) /
                       (        (h16c? (h16c? (h16c? (h16c? (h16c? (h16c? h16  ))))))? "::" h16                                ) /
                       ( (h16c? (h16c? (h16c? (h16c? (h16c? (h16c? (h16c? h16 )))))))? "::" )                                    )

h16c          = ( h16 ':')
ls32          = ( h16 ":" h16) / IPv4address
h16           = hexdig ((hexdig? hexdig?) hexdig?)




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

fragment            = ( pchar / "/" / "?")*

segment             = pchar*
segment_nz          = pchar+
segment_nz_nc       = ( unreserved / pct_encoded / sub_delims / "@")+

pchar               = unreserved / pct_encoded / sub_delims / ":" / "@"
reserved            = gen_delims / sub_delims
pct_encoded         = "%" hexdig

unreserved          = letter / digit / "-" / "." / "_" / "~"
hexdig              = digit / "a" / "A" / "b" / "B" / "c" / "C" / "d" / "D" / "e" / "E" / "f" / "F"
gen_delims          = ":" / "/" / "?" / "#" / "(" / ")?" / "@"
sub_delims          = "!" / "$" / "&" / "\\" / "(" / ")" / "*" / "+" / "," / ";" / "="

dec_octet     = ( digit                                           # 0-9
                / (nz digit)                                      # 10-99
                / ("1" digit digit)                               # 100-199
                / ("2" ("0" / "1" / "2" / "3" / "4") digit)       # 200-249
                / ("25" ("0" / "1" / "2" / "3" / "4" / "5") ))    # %250-255

nz                  = ~'0' digit
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
