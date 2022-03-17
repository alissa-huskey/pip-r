from os import environ
import pytest

from pip_r.preprocess import Preprocessor, EnvVar, grammar
from pip_r.grammar import groups

from tests.stubs import Stub

@pytest.mark.parametrize("text, count, names", [
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
        assert doc[var]

def test_env_var():
    environ["STAR"] = "*"
    node = Stub(text="STAR", start=8, end=12)
    var = EnvVar(node)

    assert var.placeholder == "${STAR}"
    assert var.name == "STAR"
    assert var.value == "*"
    assert var.replace("twinkle twinkle little ${STAR}") == "twinkle twinkle little *"

@pytest.mark.parametrize("data", [
    Stub(
        env_vars=dict(COLOR="gray", R="100", G="100", B="100"),
        input="The color ${COLOR} is (${R}, ${G}, ${B}).",
        expected="The color gray is (100, 100, 100).",
    ),
    Stub(
        env_vars=dict(HOME="/Users/dev"),
        input="${HOME} sweet ${HOME}.",
        expected="/Users/dev sweet /Users/dev.",
    ),
    Stub(
        env_vars={},
        input="Oh hai there.",
        expected="Oh hai there.",
    ),
])
def test_replace(data):
    environ.update(data.env_vars)
    text = data.input

    parser = Preprocessor(text)
    doc = parser.parse()
    assert parser.process() == data.expected
