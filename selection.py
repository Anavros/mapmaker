
import cube


class Selection:
    def __init__(self, bound):
        self.q = 0
        self.r = 0
        self.s = 0
        self.cube = cube.CubePoint()
        self.bound = bound
        self.radius = 1
        self.max_radius = 18
        self.min_radius = 0

    def center(self):
        return self.cube.coordinates()

    def cube(self):
        return self.q, self.r, self.s

    def get_selected_coordinates(self):
        return cube.rings(self.radius, self.center())

    def move(self, direction, steps=1):
        self.q, self.r, self.s = cube.bounded_shift(self.center(), self.bound, direction, steps)

    def expand(self, n=1):
        self.radius = min(self.max_radius, self.radius + n)

    def contract(self, n=1):
        self.radius = max(self.min_radius, self.radius - n)
