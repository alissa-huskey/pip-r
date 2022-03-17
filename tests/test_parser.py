import pytest
from parsimonious.grammar import Grammar

from pip_r.grammar import spec, groups
from pip_r.parser import Parser

from pip_r.grammar import spec

grammar = Grammar(spec)

def test_name():
    tree = grammar.parse("""
pynvim
pytest
    """)
    parser = Parser()
    doc = parser.visit(tree)

    assert len(doc) == 2

    assert doc[0].name == "pynvim"
    assert doc[1].name == "pytest"

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

