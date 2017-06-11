
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
        self.n = n
        self.size = size
        self.q = 0
        self.r = 0
        self.s = 0
        self.radius = 1
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
            if tile is not None:
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

    def select_neighbors(self):
        for tile in self.neighbors():
            if tile is not None:
                self.selections.append(tile.cubal())

    def move_selections(self, direction):
        new_selections = []
        for key in self.selections:
            q, r, s = key
            if direction == 'north':
                if s-1 >= -self.n and r+1 <= self.n:
                    s -= 1
                    r += 1
            elif direction == 'south':
                if r-1 >= -self.n and s+1 <= self.n:
                    s += 1
                    r -= 1
            elif direction == 'northeast':
                if s-1 >= -self.n and q+1 <= self.n:
                    q += 1
                    s -= 1
            elif direction == 'northwest':
                if q-1 >= -self.n and r+1 <= self.n:
                    q -= 1
                    r += 1
            elif direction == 'southeast':
                if r-1 >= -self.n and q+1 <= self.n:
                    r -= 1
                    q += 1
            elif direction == 'southwest':
                if q-1 >= -self.n and s+1 <= self.n:
                    s += 1
                    q -= 1
            # TODO: remove extra selections if they go off the edge.
            new_selections.append((q, r, s))
        self.selections = new_selections
            
    def move(self, direction):
        if direction == 'north':
            if self.s-1 >= -self.n and self.r+1 <= self.n:
                self.s -= 1
                self.r += 1
        elif direction == 'south':
            if self.r-1 >= -self.n and self.s+1 <= self.n:
                self.s += 1
                self.r -= 1
        elif direction == 'northeast':
            if self.s-1 >= -self.n and self.q+1 <= self.n:
                self.q += 1
                self.s -= 1
        elif direction == 'northwest':
            if self.q-1 >= -self.n and self.r+1 <= self.n:
                self.q -= 1
                self.r += 1
        elif direction == 'southeast':
            if self.r-1 >= -self.n and self.q+1 <= self.n:
                self.r -= 1
                self.q += 1
        elif direction == 'southwest':
            if self.q-1 >= -self.n and self.s+1 <= self.n:
                self.s += 1
                self.q -= 1
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
