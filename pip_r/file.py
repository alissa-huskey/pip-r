class File:
    def __init__(self, filename):
        self.file = filename

    @property
    def content(self):
        with open(self.file) as fp:
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

