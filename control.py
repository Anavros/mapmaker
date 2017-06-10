
import rocket
import rocket.aux as parts
from uuid import uuid4


def go_to_tile(camera, cubemap, q, r, s):
    x, y, z = cubemap[q, r, s]
    jump_to_world_coordinate(camera, x, y)


def jump_to_world_coordinate(camera, x, y):
    camera.reset()
    camera.move(-x, -y)
    camera.set()


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


def move_by_tile(camera, world, cubemap, key, refresh):
    if key in "WSADQE":
        if key == 'W':
            camera.s -= 1
            camera.r += 1
        elif key == 'S':
            camera.s += 1
            camera.r -= 1
        elif key == 'D':
            camera.r -= 1
            camera.q += 1
        elif key == 'A':
            camera.s += 1
            camera.q -= 1
        elif key == 'Q':
            camera.q -= 1
            camera.r += 1
        elif key == 'E':
            camera.q += 1
            camera.s -= 1
        try:
            tile = cubemap[camera.q, camera.r, camera.s]
        except KeyError:
            return
        x, y, z = tile.pixel()
        jump_to_world_coordinate(camera, x, y)

    elif key in "IO":
        if key == 'I':
            # There are going to be some problems to work out with the rotation.
            # Basically we need to rotate the camera around the current tile.
            # And we need to rotate the controls as well.
            camera.rotation = (camera.rotation - 15) % 360
        if key == 'O':
            camera.rotation = (camera.rotation + 15) % 360
        world.reset()
        world.rotate(z = camera.rotation)
        refresh()

    elif key in "JK":
        try:
            tile = cubemap[camera.q, camera.r, camera.s]
        except KeyError:
            return
        if key == 'J':
            tile.down()
        elif key == 'K':
            tile.up()
        refresh()


class Camera(parts.View):
    def __init__(self):
        parts.View.__init__(self, fov=30, near=0.1)
        self.q = 0
        self.r = 0
        self.s = 0
        self.tilt = 30
        self.rotation = 15
        self.height = 1
        self.set()

    def set(self):
        self.move(z = -self.height)
        self.rotate(y = -self.tilt)
        self.move(y = self.tilt/60)
