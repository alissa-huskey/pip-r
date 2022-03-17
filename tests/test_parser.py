import pytest
from parsimonious.grammar import Grammar

from pip_r.grammar import spec, groups
from pip_r.parser import Parser

from pip_r.grammar import spec

bp = breakpoint

grammar = Grammar(spec)

def test_name():
    tree = grammar.parse("""
pynvim
pytest
    """)
    parser = Parser()
    doc = parser.visit(tree)
    results = groups(tree)


    assert len(doc) == 2

    assert doc[0].name == "pynvim"
    assert doc[1].name == "pytest"

def test_extras():
    tree = grammar.parse("SomeProject[foo, bar]")
    parser = Parser()
    doc = parser.visit(tree)

    assert doc[0].extras == "[foo, bar]"

def test_url():
    tree = grammar.parse("pip @ file:///localbuilds/pip-1.3.1.zip")
    parser = Parser()
    doc = parser.visit(tree)

    assert doc[0].URI == "file:///localbuilds/pip-1.3.1.zip"

def test_comment():
    tree = grammar.parse("pip # trailing comment")
    parser = Parser()
    doc = parser.visit(tree)

    assert doc[0].comment == "# trailing comment"

@pytest.mark.parametrize("line, versionspec", [
    ("docopt == 0.6.1", "== 0.6.1"),
    ("keyring >= 4.1.1", ">= 4.1.1"),
    ("coverage != 3.5", "!= 3.5"),
    ("Mopidy-Dirble \t ~=  1.1", "~=  1.1"),
    ("Mopidy-Dirble \t ~=  1.1", "~=  1.1"),
    ("pkg3>=1.0,<=2.0", ">=1.0,<=2.0"),
])
def test_versionspec(line, versionspec):
    tree = grammar.parse(line)
    parser = Parser()
    doc = parser.visit(tree)

    assert doc[0].versionspec == versionspec

@pytest.mark.parametrize("line, name, marker", [
    ('argparse;python_version<"2.7"', 'argparse', ';python_version<"2.7"'),
    ("name; os_name=='a' and os_name=='b'", 'name', "; os_name=='a' and os_name=='b'"),
    ("name; os_name=='a' or os_name=='b'", 'name', "; os_name=='a' or os_name=='b'"),
    ("name; os_name=='a' and os_name=='b' or os_name=='c'", 'name', "; os_name=='a' and os_name=='b' or os_name=='c'"),
    ("name; os_name=='a' or os_name=='b' and os_name=='c'", 'name', "; os_name=='a' or os_name=='b' and os_name=='c'"),
    ("name; os_name=='a' and (os_name=='b' or os_name=='c')", "name", "; os_name=='a' and (os_name=='b' or os_name=='c')"),
    ("name; (os_name=='a' or os_name=='b') and os_name=='c'", "name", "; (os_name=='a' or os_name=='b') and os_name=='c'"),
])
def test_markers(line, name, marker):
    tree = grammar.parse(line)
    parser = Parser()
    doc = parser.visit(tree)

    assert doc[0].marker == marker

