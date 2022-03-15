"""
Tests of various requirements.txt formats.

(Primarily tests pkg_resources.parse_requirements() for documentation.)
"""

import os
from pkg_resources.extern.packaging.requirements import InvalidRequirement, Requirement

import pytest

from pip_r.line import Line

from tests.stubs import Stub

class Data(Stub):
    extras = ()
    url = None
    marker = None
    specs = []
    specifier = ""
    bp = False
    skip = False


os.environ["X_VERSION"] = "1.0.0"

@pytest.mark.parametrize("params", [
    Data(text="green", name="green"),
    Data(text="pytz # with comment", name="pytz"),
    Data(
        text="console==2.9",
        name="console",
        specifier="==2.9",
        specs=[("==", "2.9",)],
    ),
    Data(
        text="console!=2.9",
        name="console",
        specifier="!=2.9",
        specs=[("!=", "2.9",)],
    ),
    Data(
        text="console>=2.9",
        name="console",
        specifier=">=2.9",
        specs=[(">=", "2.9",)],
    ),
    Data(
        text="console<=2.9",
        name="console",
        specifier="<=2.9",
        specs=[("<=", "2.9",)],
    ),
    Data(
        text="console~=2.9",
        name="console",
        specifier="~=2.9",
        specs=[("~=", "2.9",)],
    ),
    Data(
        text="console===2.9",
        name="console",
        specifier="===2.9",
        specs=[("===", "2.9",)],
    ),
    Data(
        text="console===2.9",
        name="console",
        specifier="===2.9",
        specs=[("===", "2.9",)],
    ),
    Data(
        text="console==2",
        name="console",
        specifier="==2",
        specs=[("==", "2",)],
    ),
    Data(
        text="console==2.1.3",
        name="console",
        specifier="==2.1.3",
        specs=[("==", "2.1.3",)],
    ),
    Data(
        text="console==2.1.*",
        name="console",
        specifier="==2.1.*",
        specs=[("==", "2.1.*",)],
    ),
    Data(
        text="console==2.*.*",
        name="console",
        specifier="==2.*.*",
        specs=[("==", "2.*.*",)],
    ),
    Data(
        text="console==2.2.post3",
        name="console",
        specifier="==2.2.post3",
        specs=[("==", "2.2.post3",)],
    ),
    Data(
        text="console==2.2.2.2",
        name="console",
        specifier="==2.2.2.2",
        specs=[("==", "2.2.2.2",)],
    ),
    Data(
        text="toml == 0.10.2",
        name="toml",
        specifier="==0.10.2",
        specs=[("==", "0.10.2")],
    ),
    Data(
        text='pretty-errors ; os_name == "posix"',
        name="pretty-errors",
        marker='os_name == "posix"',
    ),
    Data(
        text='pretty-errors ; os.name == "posix"',
        name="pretty-errors",
        marker='os_name == "posix"',
    ),
    Data(
        text='pretty-errors ; platform_release == "3.14.1-x86_64"',
        name="pretty-errors",
        marker='platform_release == "3.14.1-x86_64"',
    ),
    Data(
        text='pretty-errors ; platform_system == "Linux"',
        name="pretty-errors",
        marker='platform_system == "Linux"',
    ),
    Data(
        text='pretty-errors ; platform_version == "25.51-b03"',
        name="pretty-errors",
        marker='platform_version == "25.51-b03"',
    ),
    Data(
        text='pretty-errors ; python_version < "2.4"',
        name="pretty-errors",
        marker='python_version < "2.4"',
    ),
    Data(
        text='pretty-errors ; python_full_version == "3.5.0b1"',
        name="pretty-errors",
        marker='python_full_version == "3.5.0b1"',
    ),
    Data(
        text='pretty-errors ; implementation_name == "cpython"',
        name="pretty-errors",
        marker='implementation_name == "cpython"',
    ),
    Data(
        text='pretty-errors ; implementation_version == "3.4.0"',
        name="pretty-errors",
        marker='implementation_version == "3.4.0"',
    ),
    Data(
        text='pretty-errors ; extra == "test"',
        name="pretty-errors",
        marker='extra == "test"',
    ),
    Data(
        text='pretty-errors ; platform_machine == "x86_64"',
        name="pretty-errors",
        marker='platform_machine == "x86_64"',
    ),
    Data(
        text="xdoctest >= 0.10.0, <0.15.0",
        name="xdoctest",
        specifier="<0.15.0,>=0.10.0",
        specs=[('>=', '0.10.0'), ('<', '0.15.0')],
    ),
    Data(
        text="requests[security]",
        name="requests",
        extras=("security",)
    ),
    Data(
        text='asciinema[foo]>1.0;python_version<"2.7"',
        name="asciinema",
        extras=("foo",),
        specifier=">1.0",
        specs=[(">", "1.0")],
        marker='python_version < "2.7"',
    ),
    Data(
        text='pathlib2>=2.3.3,<3;python_version < "3.4" and sys.platform != "win32"',
        name="pathlib2",
        specifier="<3,>=2.3.3",
        specs=[(">=", "2.3.3"), ("<", "3")],
        marker='python_version < "3.4" and sys_platform != "win32"',
    ),
    Data(
        text="pip @ https://github.com/pypa/pip/archive/1.3.1.zip#sha1=da9234ee9982d4bbb3c72346a6de940a148ea686",
        name="pip",
        url="https://github.com/pypa/pip/archive/1.3.1.zip#sha1=da9234ee9982d4bbb3c72346a6de940a148ea686",
    ),
    Data(
        text="absl-py @ file:///tmp/build/80754af9/absl-py_1607439979954/work",
        name="absl-py",
        url="file:///tmp/build/80754af9/absl-py_1607439979954/work",
    ),
    Data(
        text="pip @ file:///localbuilds/pip-1.3.1.zip",
        name="pip",
        url="file:///localbuilds/pip-1.3.1.zip",
    ),
    Data(
        text="pip @ file:///localbuilds/pip-1.3.1-py33-none-any.whl",
        name="pip",
        url="file:///localbuilds/pip-1.3.1-py33-none-any.whl",
    ),
    Data(
        text="pip @ git+https://github.com/pypa/pip.git@7921be1537eac1e97bc40179a57f0349c2aee67d",
        name="pip",
        url="git+https://github.com/pypa/pip.git@7921be1537eac1e97bc40179a57f0349c2aee67d",
    ),
    Data(
        text='flake8==3.5.0 --install-option="--install-scripts=/usr/local/bin"',
        skip = "not supported: per-requirement options",
    ),
    Data(
        text="FooProject == 1.2 --hash=sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        skip = "not supported: hash checking mode",
    ),
    Data(
        text="--pre",
        skip = "not supported: global options"
    ),
    Data(
        text="something \\",
        skip = "not supported: line continuation",
    ),
    Data(
        text="-e https://github.com/foo/bar.git#egg=bar",
        skip = "not supported: -E REQUIREMENT"
    ),
    Data(
        text="-r other.txt",
        skip = "not supported: -r FILE"
    ),
    Data(
        text="./downloads/numpy-1.9.2-cp34-none-win32.whl",
        skip = 'not supported: a plain file with no "name @ " prefix'
    ),
    Data(
        text="-c other.txt",
        skip = "not supported: -c FILE",
    ),
    Data(
        text="iniconfig==${X_VERSION}",
        name="iniconfig",
        specifier="==1.0.0",
        specs=[("==", "1.0.0")],
        skip = "apparently parsing env vars doens't work"
    ),
])
def test_parse_valid(params):
    """This is really testing the parse_requirement function for documentation."""
    if params.skip:
        pytest.skip(params.skip)

    line = Line("requirements.txt", 1, params.text)
    req = line.parse()

    if params.bp:
        breakpoint()

    assert line.is_valid
    assert not line.is_empty
    assert isinstance(req, Requirement)
    assert line.req == req
    assert req.name == params.name
    assert req.key == params.name
    assert req.project_name == params.name
    assert req.unsafe_name == params.name
    assert req.extras == params.extras
    assert req.url == params.url
    assert str(req.specifier) == params.specifier
    assert sorted(req.specs) == sorted(params.specs)

    if params.marker:
        assert str(req.marker) == params.marker
    else:
        assert not req.marker

@pytest.mark.parametrize("params", [
    Data(text="# a comment"),
    Data(text=""),
    Data(text="  "),
])
def test_parse_empty(params):
    line = Line("requirements.txt", 1, params.text)
    req = line.parse()

    if params.bp:
        breakpoint()

    assert line.is_empty
    assert not line.req
    assert not req


@pytest.mark.parametrize("params", [
    Data(text="!32jlkfj"),
    Data(text="console ~= 1"),
    Data(text="console => 2"),
    Data(text='"dog" ~= "fred"'),
    Data(text='python_version ~= "surprise"'),
    Data(text='pretty-errors ; platform_machine == x86_64'),
    Data(text='pretty-errors ; not_a_marker == "invalid"'),
])
def test_parse_error(params):
    line = Line("requirements.txt", 1, params.text)
    req = line.parse()

    if params.bp:
        breakpoint()

    assert not line.is_valid
    assert not line.req
    assert not req
    assert isinstance(line.exception, InvalidRequirement)
    assert str(line.exception).startswith("Parse error at")
