from pkg_resources.extern.packaging.markers import UndefinedComparison

__all__ = ["Stub", "Marker", "InvalidMarker", "Requirement", "Line"]

class Stub:
    def __init__(self, *args, **kwargs):
        self.__dict__ = kwargs

class Marker(Stub):
    evaluate = lambda self: True

class InvalidMarker(Marker):
    def evaluate(self):
        raise UndefinedComparison()

class Requirement(Stub):
    marker = Marker()
    name = ""
    specifier = ""

class Line(Stub):
    req = Requirement()

