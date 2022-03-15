from os.path import isfile

from pip_r.exceptions import FileException

__all__ = ["File"]


class File:
    def __init__(self, filepath):
        if not isfile(filepath):
            raise FileException("No such file: " + filepath)

        self.path = filepath

    @property
    def content(self):
        with open(self.path) as fp:
            content = fp.read()
        return content

    @property
    def lines(self):
        if "lines" not in self.__dict__:
            self.__dict__["lines"] = self.content.splitlines(keepends=False)
        return self.__dict__["lines"]

    def __iter__(self):
        for line in self.lines:
            yield line

