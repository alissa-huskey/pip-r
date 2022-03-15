from pkg_resources import parse_requirements
from pkg_resources.extern.packaging.requirements import InvalidRequirement

from pip_r.status import Status

class Line:
    def __init__(self, file, num, content):
        self.file = file
        self.num = num
        self.content = content

        self.is_valid = True
        self.is_empty = False

        self.status = None
        self.exception = None
        self.package = None

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"Line({self.num}, {self.content!r})"

    def __bool__(self):
        return not self.is_empty

    @property
    def req(self):
        return self.parse()

    def error(self, exception):
        self.exception = exception
        self.status = Status.error
        self.is_valid = False

    def parse(self):
        try:
            results = list(parse_requirements(self.content))
        except InvalidRequirement as e:
            self.error(e)
            return

        if not results:
            self.is_empty = True
            return

        if len(results) > 1:
            self.error(Exception("More requirements than I'd expected'"))
            return

        return results[0]
