import pytest

from pip_r.status import Status

def test_status():
    assert Status.success
    assert Status("SUCCESS") == Status.success
    assert Status(0) == Status.success
    assert Status(False) == Status.success           # status 0
    assert Status(True) == Status.fail               # status 1

    with pytest.raises(KeyError) as e:
        Status("foo")
