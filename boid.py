import random
from math import pi, cos, sin, sqrt, atan2

import boid_utils as bu


class Boid:
    speed = 2
    size = (10, 24)
    colour = "white"
    view_dist = 100
    view_angle = 5 * pi / 6
    sep_dist = 24
    flock = []
    angle_divisor = 10

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

    def rotate(self, angle):
        self._update_alignment(angle)
        xc, yc = self.center
        self.p1 = (xc + self.size[0] / 2 * cos(pi / 2 + self.alignment),
                   yc + self.size[0] / 2 * sin(pi / 2 + self.alignment))
        self.p2 = (xc + self.size[0] / 2 * cos(-pi / 2 + self.alignment),
                   yc + self.size[0] / 2 * sin(-pi / 2 + self.alignment))
        self.p3 = (xc + self.size[1] * cos(self.alignment),
                   yc + self.size[1] * sin(self.alignment))
        self._update_coords()

    def move(self):
        width = self.cnv.winfo_width()
        height = self.cnv.winfo_height()

        observed = self._get_boids_in_view(Boid.flock)
        if not observed:
            rotation = bu.get_rand_rotation()
            if rotation != 0.0:
                self.rotate(rotation)
        else:
            self._align(observed)
            self._target_group_center(observed)

        dx = self.speed * cos(self.alignment)
        dy = self.speed * sin(self.alignment)

        x1, y1 = Boid._get_next_point(self.p1, dx, dy)
        x2, y2 = Boid._get_next_point(self.p2, dx, dy)
        x3, y3 = Boid._get_next_point(self.p3, dx, dy)

        x1, x2, x3 = Boid._check_wraparound(x1, x2, x3, width)
        y1, y2, y3 = Boid._check_wraparound(y1, y2, y3, height)

        self.p1 = x1, y1
        self.p2 = x2, y2
        self.p3 = x3, y3
        self._update_coords()

    def _align(self, observed):
        aligns = [boid.alignment for boid in observed]
        x_sum = sum([cos(align) for align in aligns])
        y_sum = sum([sin(align) for align in aligns])
        angle = atan2(y_sum, x_sum)
        self.rotate(angle / Boid.angle_divisor)

    def _avoid(self, observed):
        pass

    def _target_group_center(self, observed):
        centers = [boid.center for boid in observed]
        count = len(observed)
        x_sum = sum([point[0] for point in centers])
        y_sum = sum([point[1] for point in centers])
        gc = (x_sum / count, y_sum / count)
        angle = atan2(gc[1], gc[0]) - self.alignment
        self.rotate(angle / Boid.angle_divisor)

    def _unobserved_sector(self, xc, yc):
        xs = xc + self.view_dist * cos(Boid.view_angle / 2)
        ys = yc - self.view_dist * sin(Boid.view_angle / 2)
        xe = xc + self.view_dist * cos(-Boid.view_angle / 2)
        ye = yc - self.view_dist * sin(-Boid.view_angle / 2)
        return xs, ys, xc, yc, xe, ye

    def _get_distance(self, other):
        sc = self.center
        oc = other.center
        r = (sc[0] - oc[0]) ** 2 + (sc[1] - oc[1]) ** 2
        return sqrt(r)

    def _get_boids_in_view(self, boids):
        obs_boids = []
        unobserved = self._unobserved_sector(*self.center)
        for boid in boids:
            r = self._get_distance(boid)
            if r < Boid.view_dist and not bu.point_in_sector(boid.center, unobserved):
                obs_boids.append(boid)
        return obs_boids

    def _update_alignment(self, angle):
        self.alignment += angle
        if self.alignment > 2 * pi:
            self.alignment -= 2 * pi
        if self.alignment < -2 * pi:
            self.alignment += 2 * pi

    def _update_coords(self):
        x0, y0 = self.p1
        x1, y1 = self.p2
        x2, y2 = self.p3
        self.center = bu.get_center(x0, y0, x1, y1, x2, y2)
        self.cnv.coords(self.id, x0, y0, x1, y1, x2, y2)

    @staticmethod
    def _get_next_point(point, dx, dy):
        x = point[0] + dx
        y = point[1] + dy
        return x, y

    @classmethod
    def _check_wraparound(cls, p1, p2, p3, border_pos):
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

    # def r_left(self, event=None):
    #     angle = -pi / 6
    #     self.rotate(angle)
    #
    # def r_right(self, event=None):
    #     angle = pi / 6
    #     self.rotate(angle)

# rotation = bu.get_rand_rotation()
#         if rotation != 0.0:
#             self.rotate(rotation)
