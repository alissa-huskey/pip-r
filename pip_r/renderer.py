from contextlib import contextmanager
from pathlib import Path
import re

from pip_r.status import Status

class Renderer:
    dots = "." * 20
    pattern = re.compile(r'[ =><;]')

    def __init__(self, line):
        self.line = line
        self.req = line.req

    @property
    def name(self):
        if not self.req:
            return self.pattern.split(self.line.content)[0]
        return self.req.name

    @property
    def status(self):
        return self.line.status

    @property
    def message(self):
        text = ""

        if self.line.status == Status.error:
            text = self.line.exception or self.line.package.exception
            text = str(text)

        elif self.line.status == Status.skip:
            text = f"environment does not meet {self.line.req.marker}"

        elif self.line.status == Status.success:
            stdout = self.line.package.stdout
            if f"Requirement already satisfied: {self.name}" in stdout:
                text = "already installed"
            else:
                text = "installed"

        elif self.line.status == Status.fail:
            stderr = self.line.package.stderr

            text = ""
            messages = (
                ("from versions: none", "Module not found"),
                ("Could not find a version", "No version %s" % self.line.req.specifier)
            )

            for pattern, message in messages:
                if pattern in stderr:
                    text = message
                    break
            if not text:
                text = stderr

        return text

    @property
    def location(self):
        if self.status in (Status.fail, Status.error):
            path = Path(self.line.file)
            return f"[@{path.name}:{self.line.num}] "
        return ""

    def print(self, *args, **kwargs):
        print(*args, **kwargs)

    @contextmanager
    def show(self):
        #  text = "\033[33m%s\033[0m %s " % \
        text = "%s %s " % \
            (self.name, self.dots[len(self.name):])

        self.print(text, end="")

        yield

        text = "\033[%dm%-7s\033[39m %s%s" % \
            (self.status.color, self.status.name.upper(), self.location, self.message)

        self.print(text)
