
import tree
import numpy
import rocket
import rocket.aux as parts
from vispy.gloo import IndexBuffer


program = rocket.program('v.glsl', 'f.glsl')
camera = parts.View(fov=45)
world = parts.Mover()

root = None

camera.move(z=-3)


def main():
    global world, root
    root = tree.root()
    root.subdivide()
    root.subdivide()
    world.vertices, world.indices, world.colors = root.buffers()
    rocket.prep()
    rocket.launch()


@rocket.attach
def draw():
    global world
    program['xy'] = world.vertices
    program['color'] = world.colors
    program['model'] = world.transform
    program['view'] = camera.transform
    program['projection'] = camera.proj
    program.draw('triangles', IndexBuffer(world.indices))


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
