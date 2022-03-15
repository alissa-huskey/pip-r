import unittest

from pkg_resources.extern.packaging.markers import UndefinedComparison

from pip_r.status import Status
from pip_r.package import Package
from pip_r.line import Line
from pip_r import package as module

class Marker():
    def __init__(self, **kwargs):
        self.should_install = kwargs.pop("should_install", True)
        self.is_valid = kwargs.pop("is_valid", True)

    def evaluate(self):
        if not self.is_valid:
            raise UndefinedComparison()

        return self.should_install

class Requirement:
    def __init__(self, **kwargs):
        self.marker = kwargs.pop("marker", Marker(**kwargs))

class MockLine:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs

    @property
    def req(self):
        return Requirement(**self.kwargs)

class Stream():
    def read(self):
        pass

class MockPopen:
    def __init__(self, *args, **kwargs):
        self.stderr = Stream()
        self.stdout = Stream()

    def wait(self):
        pass

class MockPopenSuccess(MockPopen):
    returncode = 0

class MockPopenFail(MockPopen):
    returncode = 1

class MockPopenFailUnexpected(MockPopen):
    returncode = 2


class PackageTestCase(unittest.TestCase):
    def test_package(self):
        line = Line("requirements.txt", 1, "poetry")
        package = Package(line)

        assert package.line == line

    def test_should_install_no_marker(self):
        line = MockLine("requirements.txt", 1, "poetry", marker=None)
        package = Package(line)

        assert package.should_install()

    def test_should_install_evaluate_true(self):
        line = MockLine("requirements.txt", 1, "poetry", should_install=True)
        package = Package(line)

        assert package.should_install()

    def test_should_install_evaluate_false(self):
        line = MockLine("requirements.txt", 1, "poetry", should_install=False)
        package = Package(line)

        assert not package.should_install()

    def test_should_install_evaluate_invalid(self):
        line = MockLine("requirements.txt", 1, "poetry", is_valid=False)
        package = Package(line)

        assert not package.should_install()
        assert package.status == Status.error
        assert isinstance(package.exception, UndefinedComparison)

    def test_error(self):
        package = Package(MockLine())
        package.error(Exception())

        assert package.status == Status.error
        assert isinstance(package.exception, Exception)

    def test_skip(self):
        package = Package(MockLine())
        package.skip()

        assert package.status == Status.skip

def test_install_invalid(mocker):
    #  mocker.patch("pip_r.package.Popen", MockPopen)
    spy = mocker.spy(module, "Popen")

    line = MockLine("requirements.txt", 1, "poetry", is_valid=False)
    package = Package(line)
    status = package.install()

    assert status == Status.error
    assert not spy.call_count

def test_install_skip(mocker):
    mocker.patch("pip_r.package.Popen", MockPopen)
    spy = mocker.spy(module, "Popen")

    line = MockLine("requirements.txt", 1, "poetry", should_install=False)
    package = Package(line)
    status = package.install()

    assert status == Status.skip
    assert not spy.call_count

def test_install_success(mocker):
    mocker.patch("pip_r.package.Popen", MockPopenSuccess)
    spy = mocker.spy(module, "Popen")

    line = MockLine("requirements.txt", 1, "poetry")
    package = Package(line)
    status = package.install()

    assert status == Status.success
    assert package.code == 0
    assert spy.call_count == 1

def test_install_fail(mocker):
    mocker.patch("pip_r.package.Popen", MockPopenFail)
    spy = mocker.spy(module, "Popen")

    line = MockLine("requirements.txt", 1, "poetry", returncode=1)
    package = Package(line)
    status = package.install()

    assert spy.call_count == 1
    assert package.code == 1
    assert status == Status.fail

def test_install_fail_unexpected(mocker):
    """Test a failure with an unexpected failure exit code"""

    mocker.patch("pip_r.package.Popen", MockPopenFailUnexpected)
    spy = mocker.spy(module, "Popen")

    line = MockLine("requirements.txt", 1, "poetry", returncode=1)
    package = Package(line)
    status = package.install()

    assert spy.call_count == 1
    assert package.code == 2
    assert status == Status.fail
