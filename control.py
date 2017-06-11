
import rocket
import rocket.aux as parts
import utilities
import pickle # TODO: move saving and loading to utilities.


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


# Improve key names so you can distinguish between upper and lower, and other keys.
def handle_key_events(app, key):
    if key == '':
        return
    elif key in 'QWEASDJK':
        move_by_tile(app.camera, app.world, key)
        # TODO: don't always refresh unless needed
        # Although it might always be needed if we're moving a highlight around.
        # What we really need is a selective rerendering method.
        # But that's an optimization for later.
        app.refresh_mesh()
    elif key in 'RFIOGT':
        if key == 'R':
            app.camera.tilt(-15)
        elif key == 'F':
            app.camera.tilt(+15)
        elif key == 'I':
            app.camera.rotate(-1)
        elif key == 'O':
            app.camera.rotate(+1)
        elif key == 'G':
            app.camera.zoom(+1)
        elif key == 'T':
            app.camera.zoom(-1)
    elif key == 'P':
        utilities.screenshot_sequence()
    elif key == 'B':
        pickle.dump(app, open('world.pickle', 'wb'))


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
