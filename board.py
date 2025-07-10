import json

class Board:
    def __init__(self):
        # values, index [y][x]
        self._v = [[0]*9 for i in range(9)]

        # eliminations as a map of (x,y) -> set
        self._e = {}
        self.reset_eliminations()

        # cursor position as (x,y)
        self._cursor = (0, 0)

    def load(self, filename):
        # load the values
        with open(filename) as fp:
            self._v = json.load(fp)

        self.reset_eliminations()

    def value(self, p):
        x, y = p
        return self._v[y][x]

    def has_value(self, p):
        return self.value(p) != 0
        
    def set_value(self, p, v):
        x, y = p
        self._v[y][x] = v

    def eliminations(self, p):
        return self._e[p]

    def reset_eliminations(self):
        for x in range(9):
            for y in range(9):
                self._e[(x,y)] = set()
