from pkg_resources.extern.packaging.requirements import InvalidRequirement
from pkg_resources.extern.packaging.specifiers import SpecifierSet, InvalidSpecifier
from pkg_resources.extern.packaging.markers import Marker

from pip_r.line import Line
from pip_r.status import Status

from tests.stubs import Requirement


def test_constructor():
    line = Line("requirements.txt", 1, "green")

    assert line.file == "requirements.txt"
    assert line.num == 1
    assert line.content == "green"

def test_parse(mocker):
    def parse_requirements(string):
        return [Requirement()]

    mocker.patch("pip_r.line.parse_requirements", parse_requirements)

    line = Line("requirements.txt", 1, "green")
    req = line.parse()

    assert isinstance(req, Requirement)

def test_parse_empty(mocker):
    class Requirement: pass

    def parse_requirements(string):
        return []

    mocker.patch("pip_r.line.parse_requirements", parse_requirements)

    line = Line("requirements.txt", 2, "# a blank line")
    req = line.parse()

    assert not req
    assert not line.req
    assert line.is_empty
    assert line.is_valid

def test_parse_too_many(mocker):
    def parse_requirements(string):
        return [Requirement(), Requirement()]

    mocker.patch("pip_r.line.parse_requirements", parse_requirements)

    line = Line("requirements.txt", 3, "# no idea how this could even happen")
    req = line.parse()

    assert not req
    assert not line.req
    assert not line.is_valid
    assert line.status == Status.error

def test_parse_exception(mocker):
    def parse_requirements(string):
        raise InvalidRequirement()

    mocker.patch("pip_r.line.parse_requirements", parse_requirements)

    line = Line("requirements.txt", 3, "# no idea how this could even happen")
    req = line.parse()

    assert not req
    assert not line.req
    assert not line.is_valid
    assert line.status == Status.error

def test_name():
    line = Line(
        "requirements.txt",
        3,
        "pyflakes",
    )
    req = line.parse()

    assert line.name == "pyflakes"

def test_specifier():
    line = Line(
        "requirements.txt",
        3,
        "pyflakes >= 2.9",
    )
    req = line.parse()

    assert line.specifier == SpecifierSet(">=2.9")

def test_url():
    line = Line(
        "requirements.txt",
        3,
        "pip @ https://github.com/pypa/pip/archive/1.3.1.zip#sha1=da9234ee9982d4bbb3c72346a6de940a148ea686",
    )
    req = line.parse()

    assert line.url == "https://github.com/pypa/pip/archive/1.3.1.zip#sha1=da9234ee9982d4bbb3c72346a6de940a148ea686"

def test_marker():
    line = Line(
        "requirements.txt",
        3,
        'pretty-errors ; platform_system == "Linux"',
    )
    req = line.parse()

    assert isinstance(line.marker, Marker)
    assert str(line.marker) == str(Marker('platform_system == "Linux"'))

def test_extras():
    line = Line(
        "requirements.txt",
        3,
        'requests[security]',
    )
    req = line.parse()

    assert line.extras == ("security",)

