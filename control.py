
import rocket
import rocket.aux as parts
import utilities


class Camera():
    def __init__(self):
        self.view = parts.View(fov=30, near=0.1)
        self.x = 0
        self.y = 0
        self.angle = 30
        self.rotation = 0
        self.height = 1
        self.distance = 0
        self.refresh()

    def tilt(self, n):
        self.angle = max(0, min(30, self.angle+n))
        self.refresh()

    def jump(self, x, y):
        self.x = x
        self.y = y
        self.refresh()

    def zoom(self, n):
        self.distance = max(0, min(5, self.distance+n))
        self.refresh()

    def rotate(self, n):
        self.rotation = (self.rotation + n) % 6
        self.refresh()

    def refresh(self):
        self.view.reset()
        self.view.rotate(z = self.rotation*60)
        self.view.move(-self.x, -self.y, -self.height, absolute=True)
        self.view.rotate(y = -self.angle)
        self.view.move(y = self.angle/60)
        self.view.move(z = -(self.distance/5))


def move_by_tile(camera, world, key):
    if key in "QWEASD":
        # This changes the direction of the movement to match where the camera is facing.
        # TODO: isolate
        directions = list("WEDSAQ")
        index = directions.index(key)
        offset = camera.rotation
        result = directions[(index+offset)%6]
        mapping = {
            'W': 'north',
            'E': 'northeast',
            'Q': 'northwest',
            'S': 'south',
            'D': 'southeast',
            'A': 'southwest',
        }
        world.move(mapping[result])
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
