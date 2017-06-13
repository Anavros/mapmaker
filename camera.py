
import rocket.aux as parts


class Camera():
    def __init__(self):
        self.view = parts.View(fov=30, near=0.1)
        self.x = 0
        self.y = 0
        self.angle = 30
        self.rotation = 0
        self.height = 1
        self.distance = 5
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


