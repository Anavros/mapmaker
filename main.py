
import numpy
import random
import math
import rocket
import rocket.aux as parts
from vispy.gloo import IndexBuffer

import control
import cubemap


program = rocket.program('v.glsl', 'f.glsl')
camera = parts.View(fov=20, near=0.1)
world = parts.Mover()

camera.move(z=-3)

cm = None


def main():
    global cm
    cm = cubemap.cubemap(14, 0.03)
    refresh()
    rocket.prep(clear_color=(0.1, 0.1, 0.1))
    rocket.launch(fps=12)


def refresh():
    global cm, world
    world.vertices, world.indices, world.colors = cubemap.buffers(cm, 0.8)


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
    global camera, world
    control.free_movement(camera, world, key)
    #control.locked_movement(camera, world, key)


if __name__ == '__main__':
    main()
