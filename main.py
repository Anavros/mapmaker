
import rocket
import rocket.aux as parts


program = rocket.program('v.glsl', 'f.glsl')
camera = parts.View(fov=45)
world = parts.Mover()

camera.move(z=-6)


class Tile:
    def __init__(s, a, b, c, d, e, f, m):
        s.a = a
        s.b = b
        s.c = c
        s.d = d
        s.e = e
        s.f = f
        s.m = m


def buffers():
    vertices = [
        [-0.2, -0.2],
        [+0.2, +0.2],
        [0, 0],
    ]
    return vertices


def main():
    global world
    world.vertices = buffers()
    rocket.prep()
    rocket.launch()


@rocket.attach
def draw():
    global world
    program['xy'] = world.vertices
    program['model'] = world.transform
    program['view'] = camera.transform
    program['projection'] = camera.proj
    program.draw('points')


@rocket.attach
def key_press(key):
    global camera
    if key == 'W':
        camera.move(y = -1)
    elif key == 'S':
        camera.move(y = +1)
    elif key == 'D':
        camera.move(x = -1)
    elif key == 'A':
        camera.move(x = +1)
    elif key == 'Q':
        camera.move(z = -1)
    elif key == 'E':
        camera.move(z = +1)


if __name__ == '__main__':
    main()
