from random import random, randint, uniform
from math import pi, cos, sin, sqrt, atan2
from collections import namedtuple

Point = namedtuple("Point", "x y")
Size = namedtuple("Size", "width length")


class Boid:
    speed = 10
    size = Size(10, 24)
    colour = "white"
    view_dist = 100
    sep_dist = 100
    _view_angle = 5 * pi / 6
    _flock = []
    _angle_divisor = 5

    def __init__(self, cnv, rotation=0.0, *points, **kwargs):
        self.cnv = cnv
        self.id = cnv.create_polygon(*points, **kwargs)
        self.p1 = Point(points[0], points[1])
        self.p2 = Point(points[2], points[3])
        self.p3 = Point(points[4], points[5])
        self.center = Boid._get_center(*points)
        self.alignment = rotation
        Boid._flock.append(self)

    def __repr__(self):
        return f"align: {self.alignment:.2} cent: ({self.center[0]:.2f}, {self.center[1]:.2f})"

    def move(self):
        width = self.cnv.winfo_width()
        height = self.cnv.winfo_height()
        self._realign()
        x1, x2, x3, y1, y2, y3 = self._get_coords(width, height)
        self._update_coords(x1, x2, x3, y1, y2, y3)
        self._redraw_boid()

    def _update_coords(self, x1, x2, x3, y1, y2, y3):
        self.center = Boid._get_center(x1, y1, x2, y2, x3, y3)
        self.p1 = Point(x1, y1)
        self.p2 = Point(x2, y2)
        self.p3 = Point(x3, y3)

    def _get_coords(self, width, height):
        dx = self.speed * cos(self.alignment)
        dy = self.speed * sin(self.alignment)

        x1, y1 = Boid._get_next_point(self.p1, dx, dy)
        x2, y2 = Boid._get_next_point(self.p2, dx, dy)
        x3, y3 = Boid._get_next_point(self.p3, dx, dy)

        x1, x2, x3 = Boid._check_wraparound(x1, x2, x3, width)
        y1, y2, y3 = Boid._check_wraparound(y1, y2, y3, height)
        return x1, x2, x3, y1, y2, y3

    def _realign(self):
        observed = self._get_boids_in_view(Boid._flock)
        if not observed:
            rotation = Boid._get_rand_rotation()
            if rotation != 0.0:
                self._rotate(rotation)
        else:
            self._avoid(observed)
            self._align(observed)
            self._target_center(observed)

    def _avoid(self, observed):
        centers = [boid.center for boid in observed]
        x_sum = -1 * sum([point.x for point in centers])
        y_sum = -1 * sum([point.y for point in centers])
        angle = atan2(y_sum, x_sum)
        self._rotate(angle / Boid._angle_divisor)

    def _align(self, observed):
        aligns = [boid.alignment for boid in observed]
        x_sum = sum([cos(align) for align in aligns])
        y_sum = sum([sin(align) for align in aligns])
        angle = atan2(y_sum, x_sum)
        self._rotate(angle / Boid._angle_divisor)

    def _target_center(self, observed):
        centers = [boid.center for boid in observed]
        count = len(observed)
        x_sum = sum([point.x for point in centers])
        y_sum = sum([point.y for point in centers])
        gc = (x_sum / count, y_sum / count)
        angle = atan2(gc[1], gc[0]) - self.alignment
        self._rotate(angle / Boid._angle_divisor)

    def _rotate(self, angle):
        self._update_alignment(angle)
        xc, yc = self.center
        self.p1 = Point(xc + self.size.width / 2 * cos(pi / 2 + self.alignment),
                        yc + self.size.width / 2 * sin(pi / 2 + self.alignment))
        self.p2 = Point(xc + self.size.width / 2 * cos(-pi / 2 + self.alignment),
                        yc + self.size.width / 2 * sin(-pi / 2 + self.alignment))
        self.p3 = Point(xc + self.size.length * cos(self.alignment),
                        yc + self.size.length * sin(self.alignment))
        self._redraw_boid()

    def _get_unobserved_sector(self):
        xs = self.center.x + self.view_dist * cos(Boid._view_angle / 2)
        ys = self.center.y - self.view_dist * sin(Boid._view_angle / 2)
        xe = self.center.x + self.view_dist * cos(-Boid._view_angle / 2)
        ye = self.center.y - self.view_dist * sin(-Boid._view_angle / 2)
        return Point(xs, ys), self.center, Point(xe, ye)

    def _get_distance(self, other):
        sc = self.center
        oc = other.center
        r = (sc.x - oc.x) ** 2 + (sc.y - oc.y) ** 2
        return sqrt(r)

    def _get_boids_in_view(self, boids):
        obs_boids = []
        unobserved = self._get_unobserved_sector()
        for boid in boids:
            r = self._get_distance(boid)
            if r < Boid.view_dist and not Boid._point_in_sector(boid.center, unobserved):
                obs_boids.append(boid)
        return obs_boids

    def _update_alignment(self, angle):
        self.alignment += angle
        if self.alignment > 2 * pi:
            self.alignment -= 2 * pi
        if self.alignment < -2 * pi:
            self.alignment += 2 * pi

    def _redraw_boid(self):
        x0, y0 = self.p1
        x1, y1 = self.p2
        x2, y2 = self.p3
        self.cnv.coords(self.id, x0, y0, x1, y1, x2, y2)

    @staticmethod
    def _get_next_point(point, dx, dy):
        x = point.x + dx
        y = point.y + dy
        return Point(x, y)

    @staticmethod
    def _get_center(*points):
        return Point(1 / 3 * sum(points[::2]), 1 / 3 * sum(points[1::2]))

    @staticmethod
    def _sign(point, l_start, l_end):
        return (point.x - l_end.x) * (l_start.y - l_end.y) - (l_start.x - l_end.x) * (point.y - l_end.y)

    @staticmethod
    def _point_in_sector(point, sector):
        point1, point2, point3 = sector
        sign1 = Boid._sign(point, point1, point2)
        sign2 = Boid._sign(point, point2, point3)
        sign3 = Boid._sign(point, point3, point1)
        negative = (sign1 < 0) or (sign2 < 0) or (sign3 < 0)
        positive = (sign1 > 0) or (sign2 > 0) or (sign3 > 0)
        return not (negative and positive)

    @staticmethod
    def _get_rand_rotation():
        max_angle = 0.1
        rand = random()
        angle = uniform(-max_angle, max_angle) if rand > 0.9 else 0.0
        return angle

    @classmethod
    def _check_wraparound(cls, p1, p2, p3, border_pos):
        if p3 >= border_pos:
            p1 = -Boid.size.length
            p2 = -Boid.size.length
            p3 = 0
        elif p3 <= 0:
            p1 = border_pos + Boid.size.length
            p2 = border_pos + Boid.size.length
            p3 = border_pos
        return p1, p2, p3

    @classmethod
    def init_rand_boid(cls, canvas, c_width, c_height):
        r = uniform(0.0, 2 * pi)
        xc = randint(0, c_width)
        yc = randint(0, c_height)
        x1 = xc + cls.size.width / 2 * cos(pi / 2 + r)
        y1 = yc - cls.size.width / 2 * sin(pi / 2 + r)
        x2 = xc + cls.size.width / 2 * cos(-pi / 2 + r)
        y2 = yc - cls.size.width / 2 * sin(-pi / 2 + r)
        x3 = xc + cls.size.length * cos(r)
        y3 = yc - cls.size.length * sin(r)
        return Boid(canvas, r, x1, y1, x2, y2, x3, y3, fill=cls.colour)
