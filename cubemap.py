
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
        self.color = numpy.random.random(3)

        # Temporary for the game of life.
        self.alive = random.choice([True, False])

    def __repr__(s):
        return "Tile({}, {})".format(s.q, s.r)

    def __str__(s):
        return repr(s)

    def axial(s):
        return s.q, s.r

    def cubal(s):
        x = s.q
        z = s.r
        y = -x - z
        return x, y, z

    def pixel(s):
        x = s.size * 3/2 * s.q
        y = s.size * math.sqrt(3) * (s.r + s.q/2)
        z = s.size * s.height
        return (x, y, z)


def cubemap(n, size):
    # There's got to be a better way to do this.
    cm = {}
    for q in range(-n, n+1):
        for r in range(-n, n+1):
            for s in range(-n, n+1):
                if q+r+s == 0:
                    cm[q, r, s] = Tile(q, r, size=size)
    return cm


def neighbors(cm, x, y, z):
    """
    Find the hexagons adjacent to this one.
    """
    #if (x, y, z) not in cm:
        #return [None]*6
    n  = cm.get((x, y+1, z-1), None)
    s  = cm.get((x, y-1, z+1), None)
    ne = cm.get((x+1, y, z-1), None)
    nw = cm.get((x-1, y+1, z), None)
    se = cm.get((x+1, y-1, z), None)
    sw = cm.get((x-1, y, z+1), None)
    return [n, s, ne, nw, se, sw]


def buffers(cm, scale=1.0):
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
