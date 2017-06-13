
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

    def move_selection(self, direction, steps=1):
        """
        Shift all selections one or more steps in one direction.
        Directions include n, s, ne, nw, se, sw.
        Will not move selections outside of map boundaries.
        """
        center = (self.q, self.r, self.s)
        if cube.in_bounds_after_shift(center, self.n, direction, steps):
            self.q, self.r, self.s = cube.shift(center, direction, steps)
            new_selections = []
            for key in self.selections:
                # Extra selections are allowed to move outside the map, but they should
                # still focus around the center.
                q, r, s = cube.shift(key, direction, steps)
                new_selections.append((q, r, s))
            self.selections = new_selections


def generate(n):
    # There's got to be a better way to do this.
    # We could probably do it in rings, like the spiral algorithm.
    cm = {}
    for q in range(-n, n+1):
        for r in range(-n, n+1):
            for s in range(-n, n+1):
                if q+r+s == 0:
                    cm[q, r, s] = Tile(q, r)
    return cm


# Centers are 3 away from each other at one level up.
def chunkify(tiles, n):
    cm = {}
    cm[0, 0, 0] = tiles[0, 0, 0]
    for key in cube.spiral_traversal(tiles, n):
        t = tiles.get(key, None)
        if t is None: continue
        cm[key] = t
    return cm
