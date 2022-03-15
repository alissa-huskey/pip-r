import unittest
from os.path import dirname, join

from pip_r.file import File

def getfile(name):
    fixturedir = join(dirname(__file__), "fixtures")
    return join(fixturedir, name)

class FileTestCase(unittest.TestCase):
    def test_constructor(self):
        path = getfile("simple.txt")
        file = File(path)

        assert file.file == path
        assert file.content == '# comment\npipx >= 2.0\npytest\nipython # comment\n\n'
        assert len(file.lines) == 5

