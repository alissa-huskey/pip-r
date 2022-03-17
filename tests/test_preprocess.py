import pytest

from pip_r.preprocess import Preprocessor
from pip_r.grammar import groups

@pytest.mark.parametrize("text, count, names", [
    #  (r"pip @ ${HOME}/downloads/numpy-\${VERSION}-cp34-none-win32.whl", 1, ["HOME"]),
    ("pip @ ./downloads/numpy-1.9.2-cp34-none-win32.whl", 0, []),
    ("pip @ ${HOME}/downloads/numpy-1.9.2-cp34-none-win32.whl", 1, ["HOME"]),
    ("pip @ ${HOME}/downloads/numpy-${VERSION}-cp34-none-win32.whl", 2, ["HOME", "VERSION"]),
    ("pip @ ${HOME}/downloads/numpy-$VERSION-cp34-none-win32.whl", 1, ["HOME"]),
])
def test_grammar(text, count, names):
    tree = grammar.parse(text)
    doc = groups(tree)

    assert len(doc["env_var"]) == count
    for var in names:
        assert (var) in doc["var_name"]


@pytest.mark.parametrize("text, count, names", [
    ("pip @ ./downloads/numpy-1.9.2-cp34-none-win32.whl", 0, []),
    ("pip @ ${HOME}/downloads/numpy-1.9.2-cp34-none-win32.whl", 1, ["HOME"]),
    ("pip @ ${HOME}/downloads/numpy-${VERSION}-cp34-none-win32.whl", 2, ["HOME", "VERSION"]),
    ("pip @ ${HOME}/downloads/numpy-$VERSION-cp34-none-win32.whl", 1, ["HOME"]),
])
def test_parse(text, count, names):
    parser = Preprocessor(text)
    doc = parser.parse()

    assert len(doc) == count
    for var in names:
        assert doc.get(var)
