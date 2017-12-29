from pathlib import Path

class ParserContext:
    def __init__(self, root, includes=[], excludes=[]):
        assert(isinstance(root, str))
        assert(isinstance(includes, list))
        assert(isinstance(excludes, list))

        self.root = root
        self.includes = includes
        self.excludes = excludes

    def resolve(self, path):
        assert(isinstance(path, str))

        try:
            p = Path(path)
            p = p.resolve()
            return p
        except:
            pass


        roots = [self.root] + self.includes
        for root in roots:
            try:
                p = Path(root + "/" +path)
                p = p.resolve()
                return p
            except:
                pass

        raise Exception("can't find the file: {0}".format(path))
