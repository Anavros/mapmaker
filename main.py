
import tree
import numpy
import rocket
import rocket.aux as parts
from vispy.gloo import IndexBuffer
from uuid import uuid4


program = rocket.program('v.glsl', 'f.glsl')
camera = parts.View(fov=45, near=0.1)
world = parts.Mover()

root = None

camera.move(z=-3)


def main():
    global world, root
    root = tree.root()
    root.subdivide()
    root.subdivide()
    root.subtiles['center'].subdivide()
    world.vertices, world.indices, world.colors = root.buffers()
    rocket.prep()
    rocket.launch()


@rocket.attach
def draw():
    global world
    program['xyz'] = world.vertices
    program['color'] = world.colors
    program['model'] = world.transform
    program['view'] = camera.transform
    program['projection'] = camera.proj
    program.draw('triangles', IndexBuffer(world.indices))


@rocket.attach
def key_press(key):
    global camera
    t = 0.5
    r = 30
    if key == 'W':
        camera.move(y = -t, absolute=True)
    elif key == 'S':
        camera.move(y = +t, absolute=True)
    elif key == 'D':
        camera.move(x = -t, absolute=True)
    elif key == 'A':
        camera.move(x = +t, absolute=True)
    elif key == 'Q':
        camera.move(z = -t, absolute=True)
    elif key == 'E':
        camera.move(z = +t, absolute=True)
    elif key == 'F':
        camera.rotate(y=-r, center=True)
    elif key == 'R':
        camera.rotate(y=+r, center=True)
    elif key == 'Z':
        world.rotate(z=-60)
    elif key == 'C':
        world.rotate(z=+60)
    elif key == 'P':
        path = "/home/john/media/pictures/{}.png".format(uuid4())
        print("Saving screenshot to {}...".format(path))
        rocket.screenshot(path)


if __name__ == '__main__':
    main()
