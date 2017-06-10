
import rocket
import rocket.aux as parts
import utilities


class Camera():
    def __init__(self):
        self.view = parts.View(fov=30, near=0.1)
        self.x = 0
        self.y = 0
        self.tilt = 30
        #self.rotation = 15
        self.height = 1
        self.refresh()

    def tilt(self, n):
        self.tilt = max(0, min(45, self.tilt+n))
        self.refresh()

    def jump(self, x, y):
        self.x = x
        self.y = y
        self.refresh()

    def refresh(self):
        self.view.reset()
        self.view.move(-self.x, -self.y, -self.height)
        self.view.rotate(y = -self.tilt)
        self.view.move(y = self.tilt/60)


def tilt_camera(camera, direction):
    if direction == 'up':
        camera.tilt(-15)
    elif direction == 'down':
        camera.tilt(+15)
    else:
        raise ValueError("Unknown camera tilt direction: '{}'.".format(direction))


def move_by_tile(camera, world, key):
    if key in "WSADQE":
        mapping = {
            'W': 'north',
            'S': 'south',
            'E': 'northeast',
            'Q': 'northwest',
            'D': 'southeast',
            'A': 'southwest',
        }
        world.move(mapping[key])
        tile = world.get_current_tile()
        if tile is not None:
            x, y, z = tile.pixel()
            camera.jump(x, y)

    elif key in "JK":
        tile = world.get_current_tile()
        if tile is not None:
            if key == 'J':
                tile.down()
            elif key == 'K':
                tile.up()
