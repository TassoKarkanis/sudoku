# A generator that returns a dict with keys:
#
#  "name":         name of elimination type
#  "type":         one of "row", "column", or "square"
#  "iterator":     iterator function
#  "rep":          (x,y), a representative of the group
#  "eliminations": map of (x,y) -> set of values, indicating which cells
#                  will get which new eliminations
#
def compute_eliminations(b):
    b.reset_eliminations()
    
    # compute and yield the eliminations for all implemented types
    classes = (DirectEliminations,
               OnlyValueEliminations)
    for cls in classes:
        alg = cls(b)
        for emap in alg():
            if emap is not None:
                yield emap

# Given a board an a map of eliminations (i.e. a value returned by
# compute_eliminations()), apply them.
def apply_eliminations(b, emap):
    for p, values in emap["eliminations"].items():
        e = b.eliminations(p)
        for v in values:
            e.add(v)

def unapply_eliminations(b, emap):
    for p, values in emap["eliminations"].items():
        e = b.eliminations(p)
        for v in values:
            e.remove(v)

class BaseEliminations:
    def __init__(self, b):
        self._b = b
        self._reset()

    def _reset(self):
        self._emap = {
            "eliminations": {},
        }

    def _add(self, p, v):
        # if the cell already has a value, ignore it
        if self._b.has_value(p):
            return
        
        # ignore eliminations already stored in the board
        if v in self._b.eliminations(p):
            return
        
        # make sure the entry corresponding to p is populated
        e = self._emap["eliminations"]
        if p not in e:
            e[p] = set()

        # store the elimination
        e[p].add(v)

    def _done(self):
        # check if eliminations have been computed and reset
        emap = None
        if len(self._emap["eliminations"]) != 0:
            emap = self._emap
            self._reset()
        return emap

class DirectEliminations(BaseEliminations):
    def __init__(self, b):
        super().__init__(b)

    def __call__(self):
        # check all populated cells as eliminators
        for p in all_cells():
            # if it doesn't have a value, ignore it
            if not self._b.has_value(p):
                continue

            # check each group type
            for iterator in iterators():
                yield self._check_eliminator(p, iterator)

    def _check_eliminator(self, p0, iterator):
        self._emap["name"] = "direct"
        self._emap["type"] = iterator_name(iterator)
        self._emap["iterator"] = iterator
        self._emap["rep"] = p0
        v0 = self._b.value(p0)
        for p in iterator(p0):
            # record the elimination if not present
            if not v0 in self._b.eliminations(p):
                self._add(p, v0)
        return self._done()

class OnlyValueEliminations(BaseEliminations):
    def __init__(self, b):
        super().__init__(b)

    def __call__(self):
        # look for all unknown cells
        for p in all_cells():
            if self._b.has_value(p):
                continue

            # check each group
            for iterator in iterators():
                self._emap["name"] = "only-possible-value"
                self._emap["type"] = iterator_name(iterator)
                self._emap["iterator"] = iterator
                self._emap["rep"] = p
                self._check_cell(p, iterator)
                yield self._done()

    def _check_cell(self, p0, iterator):
        # compute the set of values
        values = set()
        for p in iterator(p0):
            v = self._b.value(p)
            if v != 0:
                values.add(v)
        
        # compute the intersection of all eliminations other than p0
        e = set([x+1 for x in range(9)])
        for p in iterator(p0):
            # ignore cells with values
            if self._b.has_value(p):
                continue
        
            # ignore p0
            if p == p0:
                continue
        
            # get the intersection
            e = e.intersection(self._b.eliminations(p))
        
        # remove the eliminations due to the values
        e = e - values
        
        # If there is only one value in the intersection of eliminations
        # and the cell admits that value, then it is definitely that value
        # (so all other values should be set as its eliminations).
        if len(e) == 1:
            v = [v for v in e][0]
            e0 = self._b.eliminations(p0)
            if v not in e0:
                # raise BaseException(f"p0: {p0} -> {v}")
                for u in all_values():
                    if v != u:
                        self._add(p0, u)

def cells_in_row(p):
    _, y = p
    for x in range(9):
        yield (x, y)

def cells_in_column(p):
    x, _ = p
    for y in range(9):
        yield (x, y)

def cells_in_square(p):
    x0, y0 = p
    for j in range(3):
        y = 3*(y0 // 3) + j
        for i in range(3):
            x = 3*(x0 // 3) + i
            yield (x, y)

def iterators():
    return (cells_in_row, cells_in_column, cells_in_square)

def iterator_name(iterator):
    names = {
        cells_in_row: "row",
        cells_in_column: "column",
        cells_in_square: "square",
    }
    return names[iterator]

def all_cells():
    for y in range(9):
        for x in range(9):
            yield (x, y)

def all_values():
    return [v+1 for v in range(9)]
        
