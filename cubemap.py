
import numpy
import random
import math


class Tile:
    def __init__(self, q, r, size=0.1):
        self.q = q  # axial coordinates
        self.r = r
        # What is size really used for here?
        self.size = size
        self.spacing = 1
        self.height = random.choice([1, 2, 3])

    def __repr__(s): return "Tile({}, {})".format(s.q, s.r)
    def  __str__(s): return repr(s)

    def axial(s):
        return s.q, s.r

    def cubal(s):
        x = s.q
        y = s.r
        z = -x - y
        return x, y, z

    def pixel(s):
        x = s.size * 3/2 * s.q
        y = s.size * math.sqrt(3) * (s.r + s.q/2)
        z = s.size * s.height
        return (x, y, z)

    def pixel_spaced(s, size):
        x = size * 3/2 * s.q
        y = size * math.sqrt(3) * (s.r + s.q/2)
        z = size * s.height
        return (x, y, z)

    def   up(self): self.height = min(5, self.height + 1)
    def down(self): self.height = max(1, self.height - 1)


class World:
    def __init__(self, n, size):
        #self.tiles = generate(n, size)
        self.chunk = {}
        self.chunk[0] = generate(n, size)
        self.chunk[1] = chunkify(self.chunk[0], n=3)
        self.chunk[2] = chunkify(self.chunk[1], n=6)
        self.level = 0
        self.n = n
        self.size = size
        self.q = 0
        self.r = 0
        self.s = 0
        self.radius = 0
        self.selections = []
        self.tiles = self.chunk[self.level]

    def upchunk(self):
        self.level = min(2, self.level + 1)
        self.tiles = self.chunk[self.level]

    def downchunk(self):
        self.level = max(0, self.level - 1)
        self.tiles = self.chunk[self.level]

    def neighbors(self):
        """
        Find the hexagons adjacent to this one. Uses None where tiles are not found.
        """
        x = self.q
        y = self.r
        z = self.s
        n  = self.tiles.get((x, y+1, z-1), None)
        s  = self.tiles.get((x, y-1, z+1), None)
        ne = self.tiles.get((x+1, y, z-1), None)
        nw = self.tiles.get((x-1, y+1, z), None)
        se = self.tiles.get((x+1, y-1, z), None)
        sw = self.tiles.get((x-1, y, z+1), None)
        return [n, s, ne, nw, se, sw]

    def get_current_tile(self):
        return self.tiles.get((self.q, self.r, self.s), None)

    def get_all_selected_tiles(self):
        current = self.get_current_tile()
        if current is None:  # problem with spacing chunks
            tiles = []
        else:
            tiles = [current]
        for key in self.selections:
            tile = self.tiles.get(key, None)
            if tile is not None and tile not in tiles:
                tiles.append(tile)
        return tiles

    def select_current_tile(self):
        current = (self.q, self.r, self.s)
        if current in self.selections:
            self.selections.remove(current)
        else:
            self.selections.append(current)

    def clear_selections(self):
        self.selections = []
        self.radius = 0

    def expand_selection(self):
        self.radius = min(16, self.radius + 1)
        self.select_within_radius()

    def contract_selection(self):
        self.radius = max(0, self.radius - 1)
        self.select_within_radius()

    def select_within_radius(self):
        n = self.radius
        # This will clear any arbitrarily selected tiles too.
        self.selections = []
        for tile in self.tiles.values():
            q, r, s = tile.cubal()
            already_included = (q, r, s) in self.selections
            nearby = abs(self.q - q) <= n and abs(self.r - r) <= n and abs(self.s - s) <= n
            if nearby and not already_included:
                self.selections.append((q, r, s))

    def move_selections(self, direction, n=1):
        new_selections = []
        for key in self.selections:
            q, r, s = key
            if direction == 'north':
                if s-n >= -self.n and r+n <= self.n:
                    s -= n
                    r += n
            elif direction == 'south':
                if r-n >= -self.n and s+n <= self.n:
                    s += n
                    r -= n
            elif direction == 'northeast':
                if s-n >= -self.n and q+n <= self.n:
                    q += n
                    s -= n
            elif direction == 'northwest':
                if q-n >= -self.n and r+n <= self.n:
                    q -= n
                    r += n
            elif direction == 'southeast':
                if r-n >= -self.n and q+n <= self.n:
                    r -= n
                    q += n
            elif direction == 'southwest':
                if q-n >= -self.n and s+n <= self.n:
                    s += n
                    q -= n
            # TODO: restore extra selections if they go off the edge and come back.
            new_selections.append((q, r, s))
        self.selections = new_selections
            
    def move(self, direction, n=1):
        if direction == 'north':
            if self.s-n >= -self.n and self.r+n <= self.n:
                self.s -= n
                self.r += n
        elif direction == 'south':
            if self.r-n >= -self.n and self.s+n <= self.n:
                self.s += n
                self.r -= n
        elif direction == 'northeast':
            if self.s-n >= -self.n and self.q+n <= self.n:
                self.q += n
                self.s -= n
        elif direction == 'northwest':
            if self.q-n >= -self.n and self.r+n <= self.n:
                self.q -= n
                self.r += n
        elif direction == 'southeast':
            if self.r-n >= -self.n and self.q+n <= self.n:
                self.r -= n
                self.q += n
        elif direction == 'southwest':
            if self.q-n >= -self.n and self.s+n <= self.n:
                self.s += n
                self.q -= n
        else:
            raise ValueError("Unknown movement direction: '{}'.".format(direction))


class Selection:
    def __init__(self):
        self.q = 0
        self.r = 0
        self.s = 0
        self.radius = 0
        self.selections = []


def generate(n, size):
    # There's got to be a better way to do this.
    # We could probably do it in rings, like the spiral algorithm.
    cm = {}
    for q in range(-n, n+1):
        for r in range(-n, n+1):
            for s in range(-n, n+1):
                if q+r+s == 0:
                    cm[q, r, s] = Tile(q, r, size=size)
    return cm


# Centers are 3 away from each other at one level up.
def chunkify(tiles, n):
    cm = {}
    cm[0, 0, 0] = tiles[0, 0, 0]
    for key in spiral_traversal(tiles, n):
        t = tiles.get(key, None)
        if t is None: continue
        replacement = Tile(t.q, t.r, size=t.size)
        replacement.height = t.height
        cm[key] = replacement
    return cm


def move_coordinates(key, direction, n):
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
        q, r, s = move_coordinates((q, r, s), 'n', n)
        start_of_next_ring = tiles.get((q, r, s), None)
        if start_of_next_ring is None:
            break
        for direction in pattern:
            for step in range(ring):
                # This will probably break for n > 1
                q, r, s = move_coordinates((q, r, s), direction, n)
                visits.append((q, r, s))
        ring += 1
    return visits
