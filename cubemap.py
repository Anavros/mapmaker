
import numpy
import random
import math


class Tile:
    # Using axial coordinates.
    def __init__(self, q, r, size=0.1):
        self.q = q
        self.r = r
        self.size = size
        self.height = random.choice([1, 2, 3])
        self.colormap = {
            1 : (0.2, 0.4, 0.6),
            2 : (0.8, 0.6, 0.4),
            3 : (0.7, 0.5, 0.3),
            4 : (0.6, 0.4, 0.2),
            5 : (0.5, 0.3, 0.1),
        }
        #self.color = numpy.random.random(3)
        self.set_color(self.colormap[self.height])
        self.highlight = False

        # Temporary for the game of life.
        self.alive = random.choice([True, False])

    def __repr__(s):
        return "Tile({}, {})".format(s.q, s.r)

    def __str__(s):
        return repr(s)

    def axial(s):
        return s.q, s.r

    def cubal(s):
        # This doesn't work right?
        # Or the tile coordinates are not being set right.
        # These don't match the map indices.
        x = s.q
        y = s.r
        z = -x - y
        return x, y, z

    def pixel(s):
        x = s.size * 3/2 * s.q
        y = s.size * math.sqrt(3) * (s.r + s.q/2)
        z = s.size * s.height
        return (x, y, z)

    def set_color(s, color):
        s.color = numpy.array(color)

    def up(self):
        self.height = min(5, self.height + 1)
        self.set_color(self.colormap[self.height])

    def down(self):
        self.height = max(1, self.height - 1)
        self.set_color(self.colormap[self.height])


class World:
    def __init__(self, n, size):
        self.tiles = generate(n, size)
        #self.tiles = chunkify(self.tiles)
        self.n = n
        self.size = size
        self.q = 0
        self.r = 0
        self.s = 0
        self.radius = 0
        self.selections = []

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
        tiles = [self.get_current_tile()]
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
            # TODO: remove extra selections if they go off the edge.
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
    cm = {}
    for q in range(-n, n+1):
        for r in range(-n, n+1):
            for s in range(-n, n+1):
                if q+r+s == 0:
                    cm[q, r, s] = Tile(q, r, size=size)
    return cm


# Centers are 3 away from each other at one level up.
def chunkify(tiles):
    cm = {}
    cm[0, 0, 0] = tiles[0, 0, 0]
    for key, tile in tiles.items():
        if sum([abs(n) for n in key]) % 6 == 0:
            # The key has (3, -3, 0) in some order.
            # Or multiples of three.
            q, r, s = [n//3 for n in key]
            cm[q, r, s] = tile
    return cm


def fits_resolution(key, r=1):
    pass


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


def buffers(cm, scale=1.0, highlights=None):
    # This is most likely temporary.
    # So we can show what tile the camera is looking at more clearly.
    if highlights is None:
        highlights = []

    vertices = []
    indices = []
    colors = []
    i = 0
    for tile in cm.values():


        size = tile.size * scale
        width = size * 2
        height = math.sqrt(3) / 2 * width
        ver = height / 2
        hor = width / 2
        half = hor/2

        # Variable prefixes:
        # i = index
        # v = vertex
        # g = ground vertex (z=0)
        # j = ground index
        ic, ie, iw, ine, inw, ise, isw = [i + n for n in range(7)]
        jc, je, jw, jne, jnw, jse, jsw = [i + n + 7 for n in range(7)]

        vc = tile.pixel()
        ve =  (vc[0]+hor, vc[1], vc[2])
        vw =  (vc[0]-hor, vc[1], vc[2])
        vne = (vc[0]+half, vc[1]+ver, vc[2])
        vnw = (vc[0]-half, vc[1]+ver, vc[2])
        vse = (vc[0]+half, vc[1]-ver, vc[2])
        vsw = (vc[0]-half, vc[1]-ver, vc[2])

        gc =  (vc[0], vc[1], 0)
        ge =  (vc[0]+hor, vc[1], 0)
        gw =  (vc[0]-hor, vc[1], 0)
        gne = (vc[0]+half, vc[1]+ver, 0)
        gnw = (vc[0]-half, vc[1]+ver, 0)
        gse = (vc[0]+half, vc[1]-ver, 0)
        gsw = (vc[0]-half, vc[1]-ver, 0)

        vertices.extend([
            vc, ve, vw, vne, vnw, vse, vsw,
            gc, ge, gw, gne, gnw, gse, gsw,
        ])

        indices.extend([
            # Top Face
            ic, ie, ine,
            ic, ine, inw,
            ic, inw, iw,
            ic, iw, isw,
            ic, isw, ise,
            ic, ise, ie,

            # Bottom Face
            jc, je, jne,
            jc, jne, jnw,
            jc, jnw, jw,
            jc, jw, jsw,
            jc, jsw, jse,
            jc, jse, je,

            # Walls
            ie, ine, jne,
            ie, jne, je,
            ine, inw, jnw,
            ine, jnw, jne,
            inw, iw, jw,
            inw, jw, jnw,
            iw, isw, jsw,
            iw, jsw, jw,
            isw, ise, jse,
            isw, jse, jsw,
            ise, ie, je,
            ise, je, jse,
        ])

        if tile.cubal() in highlights:
            colors.extend([tile.color+0.1]*7)
            colors.extend([tile.color+0.3]*7)
        else:
            colors.extend([tile.color]*7)
            colors.extend([tile.color-0.2]*7)
        i += 14
    return vertices, indices, colors


def test_neighbors(cm, x, y, z):
    cm[x, y, z].color = numpy.array((0, 0, 0))
    for tile in neighbors(cm, x, y, z):
        if tile:
            tile.color = numpy.array((1, 1, 1))


def test_cells():
    global cm
    for tile in cm.values():
        others = neighbors(cm, *tile.cubal())
        count = sum(1 for cell in others if (cell is not None) and cell.alive)

        # These changes don't happen all at once.
        # So one tile might turn on in the middle of another check or something.
        # Also, remember that there can only be up to 6 neighbors for hexes.
        if tile.alive and (count not in [2, 3]):
            tile.alive = False
        elif (not tile.alive) and (count in [3, 4, 5, 6]):
            tile.alive = True

        if tile.alive:
            tile.color = numpy.array((1, 1, 1))
            tile.height = 2
        else:
            tile.color = numpy.array((0, 0, 0))
            tile.height = 1
