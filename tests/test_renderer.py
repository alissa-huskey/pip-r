import pytest

from pip_r.renderer import Renderer
from pip_r.status import Status

class Stub:
    def __init__(self, *args, **kwargs):
        self.__dict__ = kwargs

class Line(Stub):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.req = kwargs.pop("req", Stub(**kwargs))

def test_constructor():
    line = Line()
    r = Renderer(line)

    assert r.line == line
    assert r.req == line.req

def test_name_with_req():
    line = Line(req=Stub(name="pytest"))
    r = Renderer(line)

    assert r.name == "pytest"

@pytest.mark.parametrize("content, name", [
    ("pytest >> 8", "pytest"),
    ("poetry>10", "poetry"),
    ("pip", "pip"),
])
def test_name_without_req(content, name):
    line = Line(content=content, req=None)
    r = Renderer(line)

    assert r.name == name

def test_status():
    line = Line(status = Status.success)
    r = Renderer(line)

    assert r.status == line.status

@pytest.mark.parametrize("line, message", [
    (Line(status=Status.error, exception=Exception("oh noes")), "oh noes"),
    (Line(status=Status.error, exception=None, package=Stub(exception=Exception("so sad"))), "so sad"),
    (
        Line(status=Status.skip, req=Stub(marker='os == "alien spaceship"')),
        'environment does not meet os == "alien spaceship"'
    ),
    (
        Line(status=Status.success, name="thing", package=Stub(stdout="Requirement already satisfied: thing")),
        "already installed"
    ),
    (
        Line(status=Status.success, name="thing", package=Stub(stdout="Collecting thing")),
        "installed"
    ),
    (
        Line(
            status=Status.fail,
            name="pylama",
            req=Stub(specifier="==10.0"),
            package=Stub(stderr="ERROR: Could not find a version that satisfies the requirement pylama==10.0")
        ),
        "No version ==10.0"
    ),
    (
        Line(
            status=Status.fail,
            specifier=None,
            package=Stub(stderr="ERROR: Could not find a version that satisfies the requirement missing (from versions: none)")
        ),
        "Module not found"
    ),
])
def test_message(line, message):
    r = Renderer(line)

    assert r.message == message

@pytest.mark.parametrize("status", [Status.fail, Status.error])
def test_location_not_empty(status):
    line = Line(num=2, file="requirements.txt", status=status)
    r = Renderer(line)

    assert r.location == "[@requirements.txt:2] "

@pytest.mark.parametrize("status", [Status.success, Status.skip])
def test_location_empty(status):
    line = Line(status=status)
    r = Renderer(line)

    assert r.location == ""

#  @pytest.mark.parametrize("line, name, status, location, message", [
@pytest.mark.parametrize("line, data", [
    (
        Line(
            req=Stub(name="blessed"),
            status=Status.error,
            exception=Exception("oh noes"),
            file="requirements.txt",
            num=2,
        ),
        Stub(
            before="blessed ............. ",
            after='\x1b[31mERROR  \x1b[39m [@requirements.txt:2] oh noes',
        ),
    ),
    (
        Line(
            req=Stub(name="pylint"),
            status=Status.error,
            exception=None,
            package=Stub(exception=Exception("so sad")),
            file="requirements.txt",
            num=3,
        ),
        Stub(
            before="pylint .............. ",
            after='\x1b[31mERROR  \x1b[39m [@requirements.txt:3] so sad',
        ),
    ),
    (
        Line(
            status=Status.skip,
            req=Stub(marker='os == "alien spaceship"', name="pdbpp"),
        ),
        Stub(
            before="pdbpp ............... ",
            after='\x1b[33mSKIP   \x1b[39m environment does not meet os == "alien spaceship"',
        ),
    ),
    (
        Line(
            name="thing",
            status=Status.success,
            package=Stub(stdout="Requirement already satisfied: thing"),
        ),
        Stub(
            before="thing ............... ",
            after='\x1b[32mSUCCESS\x1b[39m already installed',
        ),
    ),
    (
        Line(
            status=Status.success,
            name="thing",
            package=Stub(stdout="Collecting thing"),
        ),
        Stub(
            before="thing ............... ",
            after='\x1b[32mSUCCESS\x1b[39m installed',
        ),
    ),
    (
        Line(
            status=Status.fail,
            name="pylama",
            req=Stub(name="pylama", specifier="==10.0"),
            package=Stub(stderr="ERROR: Could not find a version that satisfies the requirement pylama==10.0"),
            file="requirements.txt",
            num=8,
        ),
        Stub(
            before="pylama .............. ",
            after='\x1b[31mFAIL   \x1b[39m [@requirements.txt:8] No version ==10.0',
        ),
    ),
    (
        Line(
            status=Status.fail,
            specifier=None,
            req=Stub(name="pylint", specifier=""),
            package=Stub(stderr="ERROR: Could not find a version that satisfies the requirement missing (from versions: none)"),
            file="requirements.txt",
            num=9,
        ),
        Stub(
            before="pylint .............. ",
            after='\x1b[31mFAIL   \x1b[39m [@requirements.txt:9] Module not found',
        ),
    ),
])
def test_show(mocker, line, data):
    r = Renderer(line)
    spy = mocker.spy(r, "print")

    with r.show():
        pass

    assert spy.call_count == 2

    first, second = spy.call_args_list
    assert (first.args, first.kwargs) == ((data.before,), {"end": ""})
    assert (second.args, second.kwargs) == ((data.after,), {})
