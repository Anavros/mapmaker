
import utilities


def single_event(app, key):
    """
    These are events that can't be repeated by holding down the key.
    """
    if key == 'P':
        utilities.screenshot_sequence()
    elif key == 'B':
        utilities.save_app(app)
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
    elif key == '1':
        app.world.downchunk()
        app.refresh_mesh()
    elif key == '2':
        app.world.upchunk()
        app.refresh_mesh()


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


def move_by_tile(camera, world, key):
    # This updates the world (q, r, s) and the camera (x, y).
    if key in "QWEASD":
        direction = rotated_movement_direction(key, camera.rotation)

        world.move_selection(direction, 1)

        tile = world.get_current_tile()
        if tile is not None:
            # Technically, we don't need to look up the tile here.
            # It's only a check that we don't move out of bounds.
            # But we could replace that with a check on the world size, world.n.
            x, y = world.cartesian_center((world.q, world.r, world.s))
            camera.jump(x, y)

    elif key in "JK":
        for tile in world.get_all_selected_tiles():
            if tile is not None:
                if key == 'J':
                    tile.down()
                elif key == 'K':
                    tile.up()
