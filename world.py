
import numpy
import random
import math
import cube


class Tile:
    def __init__(self, q, r, height=None):
        self.q = q  # axial coordinates
        self.r = r
        if height is None:
            self.height = random.choice([1, 2, 3])
        else:
            self.height = min(5, max(0, height))

    def __repr__(s): return "Tile({}, {})".format(s.q, s.r)
    def  __str__(s): return repr(s)

    # We should honestly just store the coordinates as cubal.
    # We never use axial, except for the cartesian transform.
    # We didn't use cubal before because there was a typo in the function.
    def axial(s):
        return s.q, s.r

    def cubal(s):
        x = s.q
        y = s.r
        z = -x - y
        return x, y, z

    def   up(self): self.height = min(5, self.height + 1)
    def down(self): self.height = max(1, self.height - 1)


class World:
    def __init__(self, n, size):
        self.chunk = {}
        self.chunk[0] = generate(n)
        self.chunk[1] = chunkify(self.chunk[0], n=3)
        self.chunk[2] = chunkify(self.chunk[1], n=6)
        self.level = 0
        self.tile_size = size
        self.bound = n
        self.n = n
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

    def spacing(self):
        if self.level > 0:
            return self.tile_size / (3*self.level)
        else:
            return self.tile_size

    def cartesian_center(self, key):
        """
        Return (x, y) coordinates of a given (q, r, s) tile's center.
        Takes chunk level, size, and spacing into account.
        Doesn't require tile to actually exist.
        """
        q, r, s = key
        spacing = self.spacing()
        x = spacing * 3/2 * q
        y = spacing * math.sqrt(3) * (r + q/2)
        return (x, y)

    def get_selected_tiles(self, selection):
        result = []
        for coordinate in selection.get_selected_coordinates():
            tile = self.tiles.get(coordinate, None)
            if tile is not None:
                result.append(tile)
        return result


class Selection:
    def __init__(self, bound):
        self.q = 0
        self.r = 0
        self.s = 0
        self.bound = bound
        self.radius = 1
        self.max_radius = 18
        self.min_radius = 0

    def cube(self):
        return self.q, self.r, self.s

    def get_selected_coordinates(self):
        return cube.rings(self.radius, center=(self.q, self.r, self.s))

    def move(self, direction, steps=1):
        self.q, self.r, self.s = cube.bounded_shift(self.cube(), self.bound, direction, steps)

    def expand(self, n=1):
        self.radius = min(self.max_radius, self.radius + n)

    def contract(self, n=1):
        self.radius = max(self.min_radius, self.radius - n)


def generate(n):
    tilemap = {}
    for q, r, s in cube.rings(n):
        tilemap[q, r, s] = Tile(q, r)
    return tilemap


# Centers are 3 away from each other at one level up.
def chunkify(tiles, n):
    cm = {}
    cm[0, 0, 0] = tiles[0, 0, 0]
    for key in cube.spiral_traversal(tiles, n):
        t = tiles.get(key, None)
        if t is None: continue
        cm[key] = t
    return cm
