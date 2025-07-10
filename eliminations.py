def compute_eliminations(b):
    b.reset_eliminations()
    
    # direct eliminations
    for x in range(9):
        for y in range(9):
            p = (x, y)
            compute_value_eliminations(b, p)
            
    # only-possible-value
    for p in all_cells():
        if b.has_value(p):
            continue
        
        for iterator in iterators():
            compute_only_possible_value_eliminations(b, p, iterator)
        

def compute_value_eliminations(b, p0):
    # get the eliminations
    e = b.eliminations(p0)

    # perform the direct eliminations
    for iterator in iterators():
        for p in iterator(p0):
            v = b.value(p)
            if v != 0:
                e.add(v)

def compute_only_possible_value_eliminations(b, p0, iterator):
    # compute the set of values
    values = set()
    for p in iterator(p0):
        v = b.value(p)
        if v != 0:
            values.add(v)

    # compute the intersection of all eliminations other than p0
    e = set([x+1 for x in range(9)])
    for p in iterator(p0):
        # ignore cells with values
        if b.has_value(p):
            continue

        # ignore p0
        if p == p0:
            continue

        # get the intersection
        e = e.intersection(b.eliminations(p))

    # remove the eliminations due to the values
    e = e - values

    # If there is only one value in the intersection of eliminations
    # and the cell admits that value, then it is definitely that value
    # (so all other values should be set as its eliminations).
    if len(e) == 1:
        v = [v for v in e][0]
        e0 = b.eliminations(p0)
        if v not in e0:
            # raise BaseException(f"p0: {p0} -> {v}")
            for u in all_values():
                if v != u:
                    e0.add(u)

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

def all_cells():
    for y in range(9):
        for x in range(9):
            yield (x, y)

def all_values():
    return [v+1 for v in range(9)]

def iterators():
    return (cells_in_row, cells_in_column, cells_in_square)
