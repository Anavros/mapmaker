
import rocket
from uuid import uuid4

def go_to_tile(cubemap, x, y, z): pass


def free_movement(camera, world, key, t=0.1, r=15):
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


def locked_movement(): pass
