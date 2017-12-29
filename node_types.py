import os
import re

# can be class, global variable, enum, any declaration
class Symbol:
    def __init__(self):
        self.namespace = ""  # a::b::c::symbol_name
        self.name = ""
        # where it is located:
        self.file = None  # instanceof(file, CxxFile)

    def __repr__(self):
        return "{0}::{1}".format(self.namespace, self.name)








# can be header or source
class CxxFile:
    class Type:
        source = "source"
        header = "header"

    SOURCES = ["c", "cc", "cpp"]
    HEADERS = ["h", "hpp"]

    @staticmethod
    def get_type(path):
        cpp = ".*\\.({0})".format("|".join(CxxFile.SOURCES))
        hpp = ".*\\.({0})".format("|".join(CxxFile.HEADERS))
        if re.match(cpp, path):
            return CxxFile.Type.source
        elif re.match(hpp, path):
            return CxxFile.Type.header
        else:
            return None

    def __init__(self, path, type=None):
        assert(isinstance(path, str))

        if not type:
            self.type = CxxFile.get_type(path)
        else:
            self.type = type  # instanceof CxxFile.Type

        self.path = path  # path to the file
        self.declarations = []  # list of Symbols
        self.definitions = []  # list of Symbols
        self.uses = []  # list of Symbols
        self.hasA = []  # list of Symbols
        self.holdsA = []  # list of Symbols
        self.wasA = []  # list of Symbols
        self.isA = []  # list of Symbols
        self.usesInInterface = []  # list of Symbols
        self.usesInImplementation = []  # list of Symbols

        self._includes = []
        self._classes = []
        self._structs = []
        self._vars = []
        self._enums = []

    def __repr__(self):
        return str(self.path)


class Component:
    def __init__(self):
        self.root = "" # path to the component
        self.parent = None  # component's parent, instanceof Component
        self.name = ""  # component's name
        self.path = ""  # path to the dir with component
        self.cmake = None  # instanceof CMake
        self.files = []  # list of instanceof CxxFile
        self.components = []  # list of instanceof Component

    def canonical(self):
        path = ""
        c = self
        while c:
            path += c.name
            c = c.parent
        return path

    def set_parent(self, parent):
        assert (parent is None or isinstance(parent, Component))
        self.parent = parent

    def __repr__(self):
        return str(self.path)

    def __eq__(self, other):
        assert(isinstance(other, Component))
        return other.canonical() == self.canonical()

    def  __hash__(self):
        return self.canonical()