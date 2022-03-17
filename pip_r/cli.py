import sys
from os.path import isfile

from pip_r.line import Line
from pip_r.package import Package
from pip_r.file import File
from pip_r.renderer import Renderer
from pip_r.exceptions import FileException
from pip_r.preprocess import process_file
from pip_r.parser import parse_text


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

    processor = process_file(path)
    parser = parse_text(processor.content)

    for req in parser.result:
        print(req)
