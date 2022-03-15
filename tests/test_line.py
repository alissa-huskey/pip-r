from pkg_resources.extern.packaging.requirements import InvalidRequirement

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
