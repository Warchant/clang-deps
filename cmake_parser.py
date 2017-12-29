from cmakeast import ast
from cmakeast.ast import FunctionCall, Word, TokenType, WordType
import os
from pathlib import Path
from parser_context import ParserContext


# represents cmake target
class Target:
    id = 0
    def __init__(self, name):
        Target.id += 1
        self.name = name
        self.type = None  # instanceof Target.Type
        self.files = []  # list of instanceof CxxFile
        self.link_dependencies = []  # list of instanceof Target

    def __eq__(self, other):
        return str(other) == self.name

    def __hash__(self):
        return Target.id

    def __str__(self):
        return self.name

    def __repr__(self):
        return str("target {0}: {1}".format(self.type, self.name))


# represents cmake file
class CMake:
    FILE = 'CMakeLists.txt'

    def __init__(self, path):
        assert(isinstance(path, Path))
        self.path = path  # path to the cmake file
        self.targets = {}

    def __repr__(self):
        return str(self.path)


class ParserCMake:
    def __init__(self, ctx):
        assert(isinstance(ctx, ParserContext))
        self.files = []
        self.ctx = ctx

    def add_file(self, path):
        assert(isinstance(path, str))
        self.files.append(path)

    def parse_file(self, path):
        assert(isinstance(path, str))

        path = self.ctx.resolve(path)

        cmake = CMake(path)

        content = cmake.path.read_text()
        tree = ast.parse(content)

        for stmt in tree.statements:
            assert (isinstance(stmt, FunctionCall))
            # we expect always to get target name as first line
            assert (stmt.arguments[0].type == WordType.Variable)
            # target name
            tname = stmt.arguments[0].contents

            #####
            if stmt.name.lower() in ["add_library", "add_executable"]:
                if tname in cmake.targets:
                    print(
                        "duplicate target {0} in file {1}... skipping".format(
                            tname, path))
                    continue

                target = Target(tname)

                # and then sources
                for cpp in stmt.arguments[1:]:
                    assert (isinstance(cpp, Word))
                    assert (cpp.type == WordType.CompoundLiteral)
                    p = self.ctx.resolve(cpp.contents)
                    target.files.append(p)

                cmake.targets[target.name] = target

            #####
            if stmt.name.lower() == "target_link_libraries":
                if tname not in cmake.targets:
                    print(
                        "target_link_libraries on non-existent target: {0}, file {1}:".format(
                            tname, path))

                target = cmake.targets[tname]

                for link in stmt.arguments[1:]:
                    assert (isinstance(link, Word))
                    assert (link.type == WordType.Variable), link.type
                    target.link_dependencies.append(link.contents)

        return cmake

    def parse(self):
        for p in self.files:
            self.parse_file(p)



if __name__ == '__main__':
    root_dir = "/home/bogdan/tools/iroha/"
    FILE = "/home/bogdan/tools/iroha/irohad/ametsuchi/CMakeLists.txt"

    includes = [
        os.path.join(root_dir, "irohad"),
        os.path.join(root_dir, "libs"),
        os.path.join(root_dir, "iroha-cli"),
        os.path.join(root_dir, "shared_model")
    ]

    excludes = [
        # ".*\\.[^tx]{3}$"
        "\\.i$"
    ]

    ctx = ParserContext(root_dir, includes, excludes)
    p = ParserCMake(ctx)
    c = p.parse_file(FILE)

    print(c)

