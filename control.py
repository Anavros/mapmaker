
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
        self.angle = max(0, min(45, self.angle+n))
        self.refresh()

    def jump(self, x, y):
        self.x = x
        self.y = y
        self.refresh()

    def zoom(self, n):
        self.distance = max(0, min(10, self.distance+n))
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


def repeating_event(app, key):
    if key in 'QWEASDJK':
        move_by_tile(app.camera, app.world, key)
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


def single_event(app, key):
    """
    These are events that can't be repeated by holding down the key.
    """
    if key == 'P':
        utilities.screenshot_sequence()
    elif key == 'B':
        pickle.dump(app, open('world.pickle', 'wb'))
    elif key == 'M':
        app.world.select_current_tile()
    elif key == 'N':
        app.world.clear_selections()
        app.refresh_mesh()
    elif key == 'L':
        app.world.expand_selection()
        app.refresh_mesh()
    elif key == 'H':
        app.world.contract_selection()
        app.refresh_mesh()


def select_camera_relative_movement_direction(key, rotation):
    """
    Convert a keypress into a compass direction, adjusting for camera rotation.
    So pressing 'w' will move up, regardless of where the camera is facing,
    whether up is north, south, or whatever.
    """
    directions = list("WEDSAQ")
    assert key in directions
    index = directions.index(key)
    result = directions[(index+rotation)%6]
    mapping = {
        'W': 'north',
        'E': 'northeast',
        'Q': 'northwest',
        'S': 'south',
        'D': 'southeast',
        'A': 'southwest',
    }
    return mapping[result]


def move_by_tile(camera, world, key):
    if key in "QWEASD":
        direction = select_camera_relative_movement_direction(key, camera.rotation)
        world.move(direction)
        world.move_selections(direction)
        tile = world.get_current_tile()
        if tile is not None:
            x, y, z = tile.pixel()
            camera.jump(x, y)

    elif key in "JK":
        for tile in world.get_all_selected_tiles():
            if tile is not None:
                if key == 'J':
                    tile.down()
                elif key == 'K':
                    tile.up()
