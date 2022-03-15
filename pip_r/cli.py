import sys

from pip_r.line import Line
from pip_r.package import Package
from pip_r.file import File
from pip_r.renderer import Renderer
from pip_r.exceptions import FileException


__all__ = ["error", "abort"]


def error(*msg):
    """print an error message to stderr"""
    text = " ".join(map(str, msg))
    sys.stderr.write("[Error] {}\n".format(text))


def abort(msg):
    """print an error message then exit"""
    error(msg)
    exit(1)


def main():
    if not sys.argv[1:]:
        abort("Missing required argument: FILE")

    path = sys.argv[1]

    if not isfile(path):
        abort("No such file:" + path)

    try:
        file = File(path)
    except FileException as e:
        abort(e)

    for i, string in enumerate(file.lines, 1):

        line = Line(path, i, string)
        line.parse()

        if line.is_empty:
            continue

        with Renderer(line).show():
            if line.is_valid and line.req:
                line.package = Package(line)
                line.status = line.package.install()
