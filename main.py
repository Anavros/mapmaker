
import rocket
import rocket.aux as parts

import control
import cubemap
import graphics


class Application:
    def __init__(self):
        self.camera = control.Camera()
        self.mesh = parts.Mover()
        self.world = cubemap.World(14, 0.03)
        self.refresh_mesh()

    def refresh_mesh(s):
        s.mesh.vertices, s.mesh.indices, s.mesh.colors = cubemap.buffers(s.world.tiles)


app = None


def main():
    global app
    app = Application()
    rocket.prep(clear_color=(0.1, 0.1, 0.1))
    rocket.launch(fps=12)


@rocket.attach
def draw():
    global app
    graphics.render(app.mesh, app.camera.view)


@rocket.attach
def key_press(key):
    global app
    if key == '':
        return
    elif key in 'QWEASDJK':
        control.move_by_tile(app.camera, app.world, key)
        # TODO: don't always refresh unless needed
        app.refresh_mesh()
    elif key in 'RF':
        if key == 'R':
            app.camera.tilt(-15)
        elif key == 'F':
            app.camera.tilt(+15)
    elif key in 'IO':
        if key == 'I':
            app.camera.rotate(-60)
        if key == 'O':
            app.camera.rotate(+60)


if __name__ == '__main__':
    main()
