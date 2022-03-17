import pytest

from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node

from pip_r.grammar import spec, walk, groups

grammar = Grammar(spec)

@pytest.mark.parametrize("package", [
    "pytest",
    "more-itertools",
    "send2trash",
    "iterm2",
    "some_package",
    "other.package",
    "A",
    "A.B-C_D",
    "aa",
    "name",
])
def test_plain_identifiers(package):
    tree = grammar.parse(package)
    results = groups(tree)

    assert results["specification"] == [package]
    assert results["name"] == [package]

def test_multiline_plain_identifiers():
    text = """
pytest
pynvim
 pytz
    pyflakes
"""
    tree = grammar.parse(text + "\n")
    results = groups(tree)

    assert len(results["specification"]) == 4
    assert len(results["name"]) == 4
    assert "pynvim" in results["name"]
    assert "pytest" in results["name"]
    assert "pytz" in results["name"]
    assert "pyflakes" in results["name"]

@pytest.mark.parametrize("line", [
    "_some_package",
    ".some_package",
    "-some_package",
    "some_package_",
    "some_package.",
    "some_package-",
    "some!package",
    "some:package",
    "some@package",
])
def test_plain_invalid_identifiers(line):
    # ^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$
    with pytest.raises(Exception) as e:
        tree = grammar.parse(package)

@pytest.mark.parametrize("line, name, operator, version", [
    ("docopt == 0.6.1", "docopt", "==", "0.6.1"),
    ("keyring >= 4.1.1", "keyring", ">=", "4.1.1"),
    ("coverage != 3.5", "coverage", "!=", "3.5"),
    ("Mopidy-Dirble \t ~=  1.1", "Mopidy-Dirble", "~=", "1.1"),
])
def test_versionspec(line, name, operator, version):
    tree = grammar.parse(line)
    results = groups(tree)

    assert results["specification"] == [line]
    assert results["name"] == [name]
    assert results["version_operator"] == [operator]
    assert results["version"] == [version]


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
    doc = groups(tree)

    assert doc["name"] == [name]
    assert doc["marker"] == [marker]

def test_comments():
    tree = grammar.parse(line)
    doc = groups(tree)

    assert doc["comment"] == [comment]

@pytest.mark.parametrize("line, comment", [
    ("# a comment line", "# a comment line"),
    ("  # a comment line", "# a comment line"),
    ("pytest # that's all folks!", "# that's all folks!")
])
def test_comments(line, comment):
    tree = grammar.parse("SomeProject[foo, bar]")
    doc = groups(tree)

    assert doc["name"] == ["SomeProject"]
    assert doc["extras"] == ["[foo, bar]"]


"""
"name@http://foo.com",
"name [fred,bar] @ http://foo.com ; python_version=='2.7'",
"name[quux, strange];python_version<'2.7' and platform_version=='2'",
"""
