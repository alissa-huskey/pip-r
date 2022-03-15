from subprocess import Popen, PIPE
from re import compile

from pkg_resources.extern.packaging.markers import UndefinedComparison

from pip_r.status import Status

class Package():
    def __init__(self, line):
        self.line = line
        self.req = line.req

        self.status = None
        self.code = None

    def __str__(self):
        return str(self.line)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, str(self.req))

    def should_install(self):
        try:
            return not self.req.marker or self.req.marker.evaluate()
        except UndefinedComparison as e:
            self.error(e)
            return False

    def skip(self):
        self.status = Status.skip

    def error(self, exception):
        self.status = Status.error
        self.exception = exception

    def install(self):
        if not self.should_install():
            return self.status or Status.skip

        proc = Popen(
            ['pip', 'install', "--disable-pip-version-check", str(self.req)],
            stdout=PIPE, stderr=PIPE,
            text=True,
        )
        proc.wait()
        self.code = proc.returncode
        self.stderr = proc.stderr.read()
        self.stdout = proc.stdout.read()

        return Status(bool(self.code))
