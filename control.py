
import utilities
import cube


def single_event(app, key):
    """
    These are events that can't be repeated by holding down the key.
    """
    if key == 'P':
        utilities.screenshot_sequence()
    elif key == 'B':
        utilities.save_app(app)
    elif key == 'N':
        app.selection.radius = 0
        app.refresh_mesh()
    elif key == '1':
        app.world.downchunk()
        app.refresh_mesh()
    elif key == '2':
        app.world.upchunk()
        app.refresh_mesh()


def repeating_event(app, key):
    if key in 'QWEASD':
        move_selection(app.camera, app.world, app.selection, key)
        app.refresh_mesh()
    elif key in 'JK':
        edit_world(key, app.world, app.selection)
        app.refresh_mesh()
    elif key in 'RFIOGT':
        move_camera(key, app.camera)
    elif key in 'HL':
        resize_selection(key, app.selection)
        app.refresh_mesh()


def resize_selection(key, selection):
    if key == 'L':
        selection.expand()
    elif key == 'H':
        selection.contract()


def move_camera(key, camera):
    if key == 'R':
        camera.tilt(-15)
    elif key == 'F':
        camera.tilt(+15)
    elif key == 'I':
        camera.rotate(-1)
    elif key == 'O':
        camera.rotate(+1)
    elif key == 'G':
        camera.zoom(+1)
    elif key == 'T':
        camera.zoom(-1)


def rotated_movement_direction(key, rotation):
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
        'W': 'n',
        'E': 'ne',
        'Q': 'nw',
        'S': 's',
        'D': 'se',
        'A': 'sw',
    }
    return mapping[result]


def move_selection(camera, world, selection, key):
    """
    Move the selection and the camera in one direction according to the pressed key.
    Accounts for camera rotation in movement direction.
    """
    direction = rotated_movement_direction(key, camera.rotation)

    # This prevents out-of-bounds movement by itself.
    selection.move(direction)
    x, y = cube.cartesian(selection.cube(), world.spacing())
    camera.jump(x, y)


def edit_world(key, world, selection):
    """
    Move selected tiles up or down.
    """
    for tile in world.get_selected_tiles(selection):
        if key == 'J':
            tile.down()
        elif key == 'K':
            tile.up()
