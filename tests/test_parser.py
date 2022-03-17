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
    res = groups(tree)

    parser = Parser()
    doc = parser.visit(tree)

    assert len(doc) == 2

    assert doc[0].name == "pynvim"
    assert doc[1].name == "pytest"
