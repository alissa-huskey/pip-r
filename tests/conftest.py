import pytest

from os.path import dirname, join

@pytest.fixture
def fixturedir():
    return join(dirname(__file__), "fixtures")

