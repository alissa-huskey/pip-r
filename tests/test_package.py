import unittest

from pkg_resources.extern.packaging.markers import UndefinedComparison

from pip_r.status import Status
from pip_r.package import Package
from pip_r import package as module

from tests.stubs import Stub, Line, Marker, InvalidMarker, Requirement


class IO():
    """stderr / stdout stub"""
    def read(self):
        pass


class PopenStub(Stub):
    returncode = None
    stderr, stdout = IO(), IO()

    @classmethod
    def returning(cls, code):
        """Return a subclass with a returncode of code"""
        class Klass(cls):
            returncode = code
        return Klass

    def __init__(self, *args, **kwargs):
        # remove the stderr/stdout kwargs so we can get the Streams()
        kwargs.pop("stderr", None)
        kwargs.pop("stdout", None)

        super().__init__(*args, **kwargs)

    def wait(self):
        pass


class PackageTestCase(unittest.TestCase):
    def test_package(self):
        line = Line()
        package = Package(line)

        assert package.line == line

    def test_should_install_no_marker(self):
        line = Line(marker=None)
        package = Package(line)

        assert package.should_install()

    def test_should_install_evaluate_true(self):
        package = Package(Line())

        assert package.should_install()

    def test_should_install_evaluate_false(self):
        line = Line(req=Requirement(marker=Marker(evaluate=lambda: False)))
        package = Package(line)

        assert not package.should_install()

    def test_should_install_evaluate_invalid(self):

        line = Line(req=Requirement(marker=InvalidMarker()))
        package = Package(line)

        assert not package.should_install()
        assert package.status == Status.error
        assert isinstance(package.exception, UndefinedComparison)

    def test_error(self):
        package = Package(Line())
        package.error(Exception())

        assert package.status == Status.error
        assert isinstance(package.exception, Exception)

    def test_skip(self):
        package = Package(Line())
        package.skip()

        assert package.status == Status.skip

def test_install_invalid(mocker):
    spy = mocker.spy(module, "Popen")

    line = Line(req=Requirement(marker=InvalidMarker()))
    package = Package(line)
    status = package.install()

    assert status == Status.error
    assert not spy.call_count

def test_install_skip(mocker):
    mocker.patch("pip_r.package.Popen", PopenStub)
    spy = mocker.spy(module, "Popen")

    line = Line(req=Requirement(marker=Marker(evaluate=lambda: False)))
    package = Package(line)

    status = package.install()

    assert status == Status.skip
    assert not spy.call_count

def test_install_success(mocker):
    mocker.patch("pip_r.package.Popen", PopenStub.returning(0))
    spy = mocker.spy(module, "Popen")

    line = Line(req=Requirement())
    package = Package(line)
    status = package.install()

    assert status == Status.success
    assert package.code == 0
    assert spy.call_count == 1

def test_install_fail(mocker):
    mocker.patch("pip_r.package.Popen", PopenStub.returning(1))
    spy = mocker.spy(module, "Popen")

    line = Line("requirements.txt", 1, "poetry", returncode=1)
    package = Package(line)
    status = package.install()

    assert spy.call_count == 1
    assert package.code == 1
    assert status == Status.fail

def test_install_fail_unexpected(mocker):
    """Test a failure with an unexpected failure exit code"""

    mocker.patch("pip_r.package.Popen", PopenStub.returning(2))
    spy = mocker.spy(module, "Popen")

    line = Line("requirements.txt", 1, "poetry", returncode=1)
    package = Package(line)
    status = package.install()

    assert spy.call_count == 1
    assert package.code == 2
    assert status == Status.fail
