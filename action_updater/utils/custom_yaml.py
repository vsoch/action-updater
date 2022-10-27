__author__ = "Vanessa Sochat"
__copyright__ = "Copyright 2022, Vanessa Sochat"
__license__ = "MPL 2.0"


class WrapperTransformer:
    def __init__(self, width, indent=2):
        self._width = width
        self._indent = indent

    def __call__(self, s):
        res = []
        for line in s.splitlines():
            if len(line) > self._width and " " in line:
                idx = 0
                while line[idx] == " ":
                    idx += 1
                line, rest = line.rsplit(" ", 1)
                res.append(line)
                res.append(" " * (idx + self._indent) + rest)
                continue
            res.append(line)
        return "\n".join(res) + "\n"
