
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
        self.refresh()

    def tilt(self, n):
        self.angle = max(0, min(30, self.angle+n))
        self.refresh()

    def jump(self, x, y):
        self.x = x
        self.y = y
        self.refresh()

    def rotate(self, n):
        self.rotation = (self.rotation + n) % 360
        self.refresh()

    def refresh(self):
        self.view.reset()
        self.view.rotate(z = self.rotation)
        self.view.move(-self.x, -self.y, -self.height, absolute=True)
        #self.view.rotate(y = -self.angle)
        #self.view.move(y = self.angle/60)


def move_by_tile(camera, world, key):
    if key in "WSEQDA":
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
