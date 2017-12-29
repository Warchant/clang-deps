from node_types import *
import os, re
import logging

from pprint import pprint



class ComponentParser:
    def __init__(self, root_dir, includes=[], excludes=[]):
        self.root = root_dir
        self.excludes = excludes
        self.components = {}
        self.logger = logging.getLogger(__name__)
        self.logger.info("Hey")

    def parse(self, root_dir, includes=[], excludes=[]):
        for include in includes:
            for files in os.listdir(include):


            for root, dirs, files in os.walk(include, topdown=True):
                dirs[:] = [d for d in dirs if
                           not any([re.match(i, d) for i in excludes])]


                c = self.parse_component(root, dirs, files)
                assert (isinstance(c, Component))

    def parse_dir(self, root):
        files = os.listdir(root)
        files[:] = [f for f in files if
                    not any([re.match(i, f) for i in self.excludes])]

        # filtered files
        for file in files:
            if os.path.isfile(file):





    # def parse_component(self, root):
    #     assert (isinstance(root, str))
    #
    #     parent, name = os.path.split(root)
    #
    #     c = Component()
    #     c.root = parent
    #     c.name = name
    #     c.path = root
    #
    #     for file in files:
    #         # abs path to the file
    #         path = os.path.join(root, file)
    #         cxx = CxxFile.create(path)
    #         if cxx:
    #             # this is header or source
    #             c.files.append(cxx)
    #         elif file == CMAKE_LISTS_TXT:
    #             # this is cmake file
    #             c.cmake = CMake(path)
    #         else:
    #             # self.logger.warning("{0} does not seem to be cmake or source file".format(path))
    #             continue
    #
    #     return c

if __name__ == '__main__':
    root_dir = "/home/bogdan/tools/iroha"

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

    c = ComponentParser(root_dir, includes, excludes)
