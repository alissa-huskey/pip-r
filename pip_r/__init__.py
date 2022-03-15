"""
https://pip.pypa.io/en/stable/reference/requirements-file-format/
https://newbedev.com/proper-way-to-parse-requirements-file-after-pip-upgrade-to-pip-10-x-x
https://stackoverflow.com/questions/6457794/pip-install-r-continue-past-installs-that-fail
https://stackoverflow.com/questions/49689880/proper-way-to-parse-requirements-file-after-pip-upgrade-to-pip-10-x-x
https://gist.github.com/akatrevorjay/293c26fefa24a7b812f5
"""

import sys
from os.path import isfile, join, dirname
import importlib
import time
import re
from pkg_resources import Requirement, parse_requirements

from pip_r.line import Line
from pip_r.package import Package
from pip_r.file import File
from pip_r.renderer import Renderer

# print an error message to stderr
def error(*msg):
    sys.stderr.write("[Error] {}\n".format(" ".join(msg)))

def abort(msg):
    error(msg)
    exit(1)

def main():
    if not sys.argv[1:]:
        abort("Missing required argument: FILE")

    path = sys.argv[1]

    if not isfile(path):
        abort("No such file:" + path)

    reqs, constraints, = {}, {}
    file = File(path)

    for i, string in enumerate(file.lines, 1):

        line = Line(path, i, string)
        line.parse()

        if line.is_empty:
            continue

        with Renderer(line).show():
            if line.is_valid and line.req:
                line.package = Package(line)
                line.status = line.package.install()


    #      package = Package(line)

    #      #  import pdb; pdb.set_trace()

    #      if package.is_constraint():
    #          constraints[package.name] = package
    #      else:
    #          reqs[package.name] = package

    #  # replace all requirements with their respective constraints
    #  for name, req in constraints.items():
    #      if name in reqs:
    #          reqs[name] = req

    #  for req in reqs.values():

    #      with req.show():
    #          req.install()

        # print the name and install command
        #  print("{} {}".format(req.name, req))


if __name__ == "__main__":
    main()
