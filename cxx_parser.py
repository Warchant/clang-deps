import clang, os
from pprint import pprint
from clang.cindex import Index
from clang.cindex import CursorKind
from node_types import CxxFile

DECLARATIONS = [
    CursorKind.UNEXPOSED_DECL,
    CursorKind.STRUCT_DECL,
    CursorKind.UNION_DECL,
    CursorKind.CLASS_DECL,
    CursorKind.ENUM_DECL,
    CursorKind.FIELD_DECL,
    CursorKind.ENUM_CONSTANT_DECL,
    CursorKind.FUNCTION_DECL,
    CursorKind.VAR_DECL,
    CursorKind.PARM_DECL,
    CursorKind.TYPEDEF_DECL,
    CursorKind.USING_DECLARATION,
    CursorKind.TYPE_ALIAS_DECL,
    CursorKind.TYPE_ALIAS_TEMPLATE_DECL,
    CursorKind.MODULE_IMPORT_DECL,
    CursorKind.FRIEND_DECL,
    CursorKind.DECL_STMT
]


def visitor(cursor):
    # print('visiting {0}'.format(cursor.kind))

    if cursor.kind in DECLARATIONS:
        print(cursor.kind, cursor.spelling, cursor.location)
        return
        # print(cursor.displayname)

    children = list(cursor.get_children())
    for child in children:
        visitor(child)


# def get_info(node, depth=0):
#     if depth >= 20:
#         children = None
#     else:
#         children = [get_info(c, depth+1)
#                     for c in node.get_children()]
#     return { 'id' : get_cursor_id(node),
#              'kind' : node.kind,
#              'usr' : node.get_usr(),
#              'spelling' : node.spelling,
#              'location' : node.location,
#              'extent.start' : node.extent.start,
#              'extent.end' : node.extent.end,
#              'is_definition' : node.is_definition(),
#              'definition id' : get_cursor_id(node.get_definition()),
#              'children' : children }


class CxxParser:
    def __init__(self, root, includes=[]):
        self.root = root
        self.includes = ["-I{0}".format(x) for x in includes]

    def parse_file(self, path):
        cxx = CxxFile(path)

        tu = Index.create().parse(cxx.path,
                                  args=['-x', 'c++',
                                        '-std=c++17'] + self.includes,
                                  options=clang.cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        d = list(tu.diagnostics)

        cxx = CxxFile(path)

        if len(d) > 0:
            print("There were parse errors:")
            pprint(d)
            return None
        else:
            for i in tu.get_includes():
                print(i.include)
                if self._file_in_project(i.include):
                    cxx._includes.append(i.include)
            # visitor(tu.cursor)

            pprint(cxx._includes)

    def _file_in_project(self, path):
        return path.name.startswith(self.root)


if __name__ == '__main__':
    root_dir = "/home/bogdan/tools/iroha"

    includes = [
        os.path.join(root_dir, "irohad"),
        os.path.join(root_dir, "libs"),
        os.path.join(root_dir, "iroha-cli"),
        os.path.join(root_dir, "shared_model"),
        os.path.join(root_dir, "schema")
    ]

    FILE = '/home/bogdan/tools/iroha/libs/common/files.cpp'

    parser = CxxParser(root_dir, includes)
    cxx = parser.parse_file(FILE)

    print(cxx)
