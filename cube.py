
"""
Functions dealing with cubal coordinates.
"""


def in_bounds(key, bounds):
    return all(-bounds <= n <= bounds for n in key)


def in_bounds_after_shift(key, bounds, direction, steps):
    return in_bounds(shift(key, direction, steps), bounds)


def bounded_shift(key, bounds, direction, steps):
    """
    Shift coordinates only if the result is not outside of bounds.
    Otherwise, does nothing.
    """
    if in_bounds_after_shift(key, bounds, direction, steps):
        return shift(key, direction, steps)
    else:
        return key


def shift(key, direction, n):
    movements = {
        'n' : ( 0, +n, -n),
        'ne': (+n,  0, -n),
        'se': (+n, -n,  0),
        's' : ( 0, -n, +n),
        'sw': (-n,  0, +n),
        'nw': (-n, +n,  0),
    }
    move = movements[direction]
    q, r, s = key
    q += move[0]
    r += move[1]
    s += move[2]
    return (q, r, s)


def spiral_traversal(tiles, n=1):
    visits = [(0, 0, 0)]
    q = r = s = 0
    pattern = ['se', 's', 'sw', 'nw', 'n', 'ne']
    ring = 1
    while True:
        q, r, s = shift((q, r, s), 'n', n)
        start_of_next_ring = tiles.get((q, r, s), None)
        if start_of_next_ring is None:
            break
        for direction in pattern:
            for step in range(ring):
                q, r, s = shift((q, r, s), direction, n)
                visits.append((q, r, s))
        ring += 1
    return visits
