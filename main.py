
import tree
import numpy
import rocket
import rocket.aux as parts
from vispy.gloo import IndexBuffer
from uuid import uuid4


program = rocket.program('v.glsl', 'f.glsl')
camera = parts.View(fov=45)
world = parts.Mover()

root = None

camera.move(z=-3)
world.rotate(y=-60)


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
    program['xyz'] = world.vertices
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
    elif key == 'F':
        world.rotate(y=15)
    elif key == 'R':
        world.rotate(y=-15)
    elif key == 'P':
        path = "/home/john/media/pictures/{}.png".format(uuid4())
        print("Saving screenshot to {}...".format(path))
        rocket.screenshot(path)


if __name__ == '__main__':
    main()
