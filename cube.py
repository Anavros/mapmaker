
import numpy
import random
import math
import rocket
import rocket.aux as parts
from vispy.gloo import IndexBuffer
from uuid import uuid4


program = rocket.program('v.glsl', 'f.glsl')
camera = parts.View(fov=45, near=0.1)
world = parts.Mover()

camera.move(z=-3)

cm = None


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


def main():
    global cm
    cm = cubemap(3, 0.1)
    test_neighbors(cm, 0, 0, 0)
    refresh()
    rocket.prep(clear_color=(0.1, 0.1, 0.1))
    rocket.launch(fps=12)


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
        

def refresh():
    global cm, world
    world.vertices, world.indices, world.colors = buffers(cm, 0.8)


#@rocket.attach
def update():
    test_cells()
    refresh()


@rocket.attach
def draw():
    global world, program
    program['xyz'] = world.vertices
    program['color'] = world.colors
    program['model'] = world.transform
    program['view'] = camera.transform
    program['projection'] = camera.proj
    #program.draw('points')
    program.draw('triangles', IndexBuffer(world.indices))


@rocket.attach
def key_press(key):
    global camera
    t = 0.5
    r = 15
    if key == 'W':
        camera.move(y = -t, absolute=True)
    elif key == 'S':
        camera.move(y = +t, absolute=True)
    elif key == 'D':
        camera.move(x = -t, absolute=True)
    elif key == 'A':
        camera.move(x = +t, absolute=True)
    elif key == 'Q':
        camera.move(z = +t, absolute=True)
    elif key == 'E':
        camera.move(z = -t, absolute=True)
    elif key == 'F':
        camera.rotate(y = -r, center=True)
    elif key == 'R':
        camera.rotate(y = +r, center=True)
    elif key == 'Z':
        world.rotate(z = -r)
    elif key == 'C':
        world.rotate(z = +r)
    elif key == 'P':
        path = "/home/john/media/pictures/{}.png".format(uuid4())
        print("Saving screenshot to {}...".format(path))
        rocket.screenshot(path)


if __name__ == '__main__':
    main()
