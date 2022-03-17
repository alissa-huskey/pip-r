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

@pytest.mark.skip(reason="not yet implemented")
def test_url():
    tree = grammar.parse("name@http://foo.com")
    doc = groups(tree)

    assert doc["name"] == ["name"]
    assert doc["url"] == ["http://foo.com"]

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

def test_line_continuation():
    text = """
requests [security,tests]     \
    >= 2.8.1, == 2.8.*        \
    ; python_version < "2.7"
"""

    tree = grammar.parse(text)
    results = groups(tree)

    assert len(results["specification"]) == 1
    assert results["name"] == ["requests"]
    assert results["versionspec"] == [">= 2.8.1, == 2.8.*"]
    assert results["marker"] == ['; python_version < "2.7"']

"""
"name@http://foo.com",
"name [fred,bar] @ http://foo.com ; python_version=='2.7'",
"name[quux, strange];python_version<'2.7' and platform_version=='2'",
"SomePackage[PDF] @ git+https://git.repo/SomePackage@main#subdirectory=subdir_path"
 -e "git+https://git.repo/some_repo.git#egg=subdir&subdirectory=subdir_path" # install a python package from a repo subdirectory

 # same as:
 # python setup.py --no-user-cfg install --prefix='/usr/local' --no-compile
 FooProject >= 1.2 --global-option="--no-user-cfg" \
                  --install-option="--prefix='/usr/local'" \
                  --install-option="--no-compile"

 SomeProject@git+https://git.repo/some_pkg.git@1.3.1

SomeProject@http://my.package.repo/SomeProject-1.2.3-py33-none-any.whl
SomeProject @ http://my.package.repo/SomeProject-1.2.3-py33-none-any.whl
SomeProject@http://my.package.repo/1.2.3.tar.gz

./downloads/numpy-1.9.2-cp34-none-win32.whl
http://wxpython.org/Phoenix/snapshot-builds/wxPython_Phoenix-3.0.3.dev1820+49a8884-cp34-none-win_amd64.whl

"""

