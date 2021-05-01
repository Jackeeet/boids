import random
from math import pi, cos, sin, sqrt

import boid_utils as bu


class Boid:
    speed = 2
    size = (10, 24)
    colour = "white"
    view_dist = 50
    view_angle = 5 * pi / 6
    sep_dist = 24
    flock = []

    def __init__(self, cnv, rotation=0.0, *points, **kwargs):
        self.cnv = cnv
        self.id = cnv.create_polygon(*points, **kwargs)
        self.p1 = (points[0], points[1])
        self.p2 = (points[2], points[3])
        self.p3 = (points[4], points[5])
        self.center = bu.get_center(*points)
        self.alignment = rotation
        Boid.flock.append(self)

    def __repr__(self):
        return f"al: {self.alignment:.2} cent: ({self.center[0]:.2f}, {self.center[0]:.2f})"

    def unobserved_sector(self, xc, yc):
        xs = xc + self.view_dist * cos(Boid.view_angle / 2)
        ys = yc - self.view_dist * sin(Boid.view_angle / 2)
        xe = xc + self.view_dist * cos(-Boid.view_angle / 2)
        ye = yc - self.view_dist * sin(-Boid.view_angle / 2)
        return xs, ys, xc, yc, xe, ye

    def get_distance(self, other):
        sc = self.center
        oc = other.center
        r = (sc[0] - oc[0]) ** 2 + (sc[1] - oc[1]) ** 2
        return sqrt(r)

    def get_boids_in_view(self, boids):
        obs_boids = []
        unobserved = self.unobserved_sector(*self.center)
        for boid in boids:
            r = self.get_distance(boid)
            if r < Boid.view_dist and not bu.point_in_sector(boid.center, unobserved):
                obs_boids.append(boid)
        return obs_boids

    def rotate(self, angle):
        xc, yc = self.center
        self.alignment += angle
        if self.alignment > 2 * pi:
            self.alignment -= 2 * pi
        if self.alignment < -2 * pi:
            self.alignment += 2 * pi

        self.p1 = (xc + self.size[0] / 2 * cos(pi / 2 + self.alignment),
                   yc + self.size[0] / 2 * sin(pi / 2 + self.alignment))
        self.p2 = (xc + self.size[0] / 2 * cos(-pi / 2 + self.alignment),
                   yc + self.size[0] / 2 * sin(-pi / 2 + self.alignment))
        self.p3 = (xc + self.size[1] * cos(self.alignment),
                   yc + self.size[1] * sin(self.alignment))
        self.update_coords()

    def update_coords(self):
        x0, y0 = self.p1
        x1, y1 = self.p2
        x2, y2 = self.p3
        self.center = bu.get_center(x0, y0, x1, y1, x2, y2)
        self.cnv.coords(self.id, x0, y0, x1, y1, x2, y2)

    @staticmethod
    def get_next_point(point, dx, dy):
        x = point[0] + dx
        y = point[1] + dy
        return x, y

    def move(self):
        width = self.cnv.winfo_width()
        height = self.cnv.winfo_height()

        rotation = bu.get_rand_rotation()
        if rotation != 0.0:
            self.rotate(rotation)

        dx = self.speed * cos(self.alignment)
        dy = self.speed * sin(self.alignment)

        x1, y1 = Boid.get_next_point(self.p1, dx, dy)
        x2, y2 = Boid.get_next_point(self.p2, dx, dy)
        x3, y3 = Boid.get_next_point(self.p3, dx, dy)

        x1, x2, x3 = Boid.check_wraparound(x1, x2, x3, width)
        y1, y2, y3 = Boid.check_wraparound(y1, y2, y3, height)

        self.p1 = x1, y1
        self.p2 = x2, y2
        self.p3 = x3, y3
        self.update_coords()

    @classmethod
    def check_wraparound(cls, p1, p2, p3, border_pos):
        if p3 >= border_pos:
            p1 = -Boid.size[1]
            p2 = -Boid.size[1]
            p3 = 0
        elif p3 <= 0:
            p1 = border_pos + Boid.size[1]
            p2 = border_pos + Boid.size[1]
            p3 = border_pos
        return p1, p2, p3

    @classmethod
    def init_rand_boid(cls, canvas, c_width, c_height):
        r = random.uniform(0.0, 2 * pi)
        xc = random.randint(0, c_width)
        yc = random.randint(0, c_height)
        x1 = xc + cls.size[0] / 2 * cos(pi / 2 + r)
        y1 = yc - cls.size[0] / 2 * sin(pi / 2 + r)
        x2 = xc + cls.size[0] / 2 * cos(-pi / 2 + r)
        y2 = yc - cls.size[0] / 2 * sin(-pi / 2 + r)
        x3 = xc + cls.size[1] * cos(r)
        y3 = yc - cls.size[1] * sin(r)
        return Boid(canvas, r, x1, y1, x2, y2, x3, y3, fill=cls.colour)

    @classmethod
    def set_colour(cls, colour):
        cls.colour = colour

    # def align(boid, all_boids):
    #     neighbours = boid.get_boids_in_view(all_boids)
    #     angle = 0.0
    #     for b in neighbours:
    #         angle += b.alignment
    #     angle /= len(neighbours)
    #     boid.alignment = angle

    # print(f"al:{self.alignment}, c:{self.center} p1: {self.p1}, p2: {self.p2:}, p3: {self.p3:}")

    # def r_left(self, event=None):
    #     angle = -pi / 6
    #     self.rotate(angle)
    #
    # def r_right(self, event=None):
    #     angle = pi / 6
    #     self.rotate(angle)
