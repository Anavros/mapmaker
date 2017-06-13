
import rocket
import rocket.aux as parts

import time
import pickle

import control
import cubemap
import graphics
import utilities
import camera


class Application:
    def __init__(self):
        self.camera = camera.Camera()
        self.mesh = parts.Mover()
        self.world = cubemap.World(14, 0.03)
        self.refresh_mesh()
        self.most_recent_event = time.time()

    def refresh_mesh(s):
        highs = [tile.cubal() for tile in s.world.get_all_selected_tiles()]
        bufs = graphics.buffers(s.world.tiles, 0.03, s.world.level, highs)
        s.mesh.vertices, s.mesh.indices, s.mesh.colors = bufs


app = None


def main(args):
    global app
    if args.pickle:
        app = utilities.load_app(args.pickle)
    else:
        app = Application()
    rocket.prep(clear_color=(0.1, 0.1, 0.1))
    rocket.launch(fps=24)


@rocket.attach
def draw():
    global app
    graphics.render(app.mesh, app.camera.view)


@rocket.attach
def key_press(key):
    global app
    if key == '':
        return
    #utilities.screenshot_sequence()
    control.single_event(app, key)


@rocket.attach
def key_hold(keys):
    # We need to limit how many times this is called per second.
    global app
    now = time.time()
    # Ten events per second, regardless of framerate.
    if now - app.most_recent_event > 0.1:
        app.most_recent_event = now
        for key in keys:
            if key == '':
                continue
            control.repeating_event(app, key)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("pickle", nargs='?')
    main(parser.parse_args())
