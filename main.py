
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

flat_mode = False


def main():
    global root
    root = tree.root()
    root.subdivide()
    root.subdivide()
    root.subdivide()
    #root.subtiles['center'].subdivide()
    dupes = tree.duplicate_tile_check(root)
    if dupes:
        print("There are duplicate tiles!")
    else:
        print("There are no duplicate tiles.")
    update()
    rocket.prep()
    rocket.launch()


def update():
    global world, root
    if flat_mode:
        world.vertices, world.indices, world.colors = root.flat_buffers()
    else:
        world.vertices, world.indices, world.colors = root.buffers()


@rocket.attach
def draw():
    global world, program
    program['xyz'] = world.vertices
    program['color'] = world.colors
    if flat_mode:
        nothing = numpy.eye(4)
        program['model'] = nothing
        program['view'] = nothing
        program['projection'] = nothing
    else:
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
        camera.move(z = +t, absolute=True)
    elif key == 'E':
        camera.move(z = -t, absolute=True)
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


def color_tile_at_point(point):
    global root
    tile = root.lowest_tile_at_point(point)
    if tile:
        tile.color = (1.0, 0.5, 0.8)
        update()
    else:
        print("Not Found!")


@rocket.attach
def left_click(point):
    point = rocket.screen_to_world(point)
    color_tile_at_point(point)


@rocket.attach
def left_drag(start, end, delta):
    point = rocket.screen_to_world(end)
    color_tile_at_point(point)


if __name__ == '__main__':
    main()
