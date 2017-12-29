# IROHA_DIR = '/home/bogdan/tools/iroha'
# IROHA_INCLUDED_DIRS = ["irohad", "iroha-cli", "libs", "test", "shared_model"]
# IROHA_INCLUDED_FILES = ["CMakeLists\\.txt", ".*\\.(c|cc|cpp|h|hpp)"]
#
# from pprint import pprint
# import cmakeast
# import os, re
# import networkx as nx
# import functools
#
#
#
# CMAKE = os.path.join(IROHA_DIR, "/".join(
#     ["irohad", "ametsuchi", "CMakeLists.txt"]))
#
#
#
#
#
# if __name__ == "__main__":
#     print(CMAKE)
#     with open(CMAKE, "r") as f:
#         d = f.read()
#         ast = cmakeast.ast.parse(d)
#         pprint(ast)
