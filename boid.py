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
    sep_dist = 80
    _view_angle = 5 * pi / 6
    _flock = []
    _angle_divisor = 5

    def __init__(self, cnv, rotation=0.0, *points, **kwargs):
        self.cnv = cnv
        self._id = cnv.create_polygon(*points, **kwargs)
        self._min_bounds = Point(0, 0)
        self._max_bounds = Point(cnv.winfo_width(), cnv.winfo_height())
        self._p1 = Point(points[0], points[1])
        self._p2 = Point(points[2], points[3])
        self._p3 = Point(points[4], points[5])
        self.center = Boid._get_center(*points)
        self.alignment = rotation
        Boid._flock.append(self)

    def __repr__(self):
        return f"align: {self.alignment:.2} cent: ({self.center[0]:.2f}, {self.center[1]:.2f})"

    def move(self):
        self._realign()
        self._update_coords(self._get_coords())
        self._redraw_boid()

    def _update_coords(self, coords):
        x1, x2, x3, y1, y2, y3 = coords
        self.center = Boid._get_center(x1, y1, x2, y2, x3, y3)
        self._p1 = Point(x1, y1)
        self._p2 = Point(x2, y2)
        self._p3 = Point(x3, y3)

    def _get_coords(self):
        dx = self.speed * cos(self.alignment)
        dy = self.speed * sin(self.alignment)

        x1, y1 = Boid._get_next_point(self._p1, dx, dy)
        x2, y2 = Boid._get_next_point(self._p2, dx, dy)
        x3, y3 = Boid._get_next_point(self._p3, dx, dy)

        x1, x2, x3 = Boid._check_wraparound(x1, x2, x3, self._max_bounds.x)
        y1, y2, y3 = Boid._check_wraparound(y1, y2, y3, self._max_bounds.y)
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
        centers = [boid.center for boid in observed if self._get_distance(boid) <= self.sep_dist]
        x_sum = -1 * sum([point.x for point in centers])
        y_sum = -1 * sum([point.y for point in centers])
        angle = atan2(y_sum, x_sum)
        self._rotate(angle / Boid._angle_divisor)

    def _align(self, observed):
        aligns = [boid.alignment for boid in observed]
        x_sum = sum([cos(align) for align in aligns])
        y_sum = sum([sin(align) for align in aligns])
        angle = atan2(y_sum, x_sum)
        # angle = sum(align for align in aligns) / len(observed)
        self._rotate(angle / Boid._angle_divisor)

    def _target_center(self, observed):
        centers = [boid.center for boid in observed]
        count = len(observed)
        x_sum = sum([point.x for point in centers])
        y_sum = sum([point.y for point in centers])
        groupcenter = (x_sum / count, y_sum / count)
        angle = atan2(groupcenter[1], groupcenter[0]) - self.alignment
        self._rotate(angle / Boid._angle_divisor)

    def _rotate(self, angle):
        self.alignment += angle
        xc, yc = self.center
        self._p1 = Point(xc + self.size.width / 2 * cos(pi / 2 + self.alignment),
                         yc + self.size.width / 2 * sin(pi / 2 + self.alignment))
        self._p2 = Point(xc + self.size.width / 2 * cos(-pi / 2 + self.alignment),
                         yc + self.size.width / 2 * sin(-pi / 2 + self.alignment))
        self._p3 = Point(xc + self.size.length * cos(self.alignment),
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

    def _redraw_boid(self):
        x0, y0 = self._p1
        x1, y1 = self._p2
        x2, y2 = self._p3
        self.cnv.coords(self._id, x0, y0, x1, y1, x2, y2)

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

    # def write_info(self):
    #     if not Boid._flock.index(self) == 0:
    #         return
    #
    #     if Boid._itercount > 100:
    #         return
    #
    #     if Boid._itercount == 0:
    #         with open("aligns.txt", "w") as f:
    #             f.write(f"Iteration 0\n")
    #             for boid in Boid._flock:
    #                 al = round(boid.alignment, 2)
    #                 s = f"{al:,.2f}\n"
    #                 f.write(s)
    #     else:
    #         with open("aligns.txt", "a") as f:
    #             f.write(f"Iteration {Boid._itercount}\n")
    #             for boid in Boid._flock:
    #                 al = round(boid.alignment, 2)
    #                 s = f"{al:,.2f}\n"
    #                 f.write(s)
    #     Boid._itercount += 1

    # @classmethod
    # def write_pos(cls):
    #     if Boid._itercount > 200:
    #         return
    #
    #     boid = Boid._flock[0]
    #     if Boid._itercount == 0:
    #         with open("pos.txt", "w") as f:
    #             s = f"{boid.center.x:,.2f}, {boid.center.y:,.2f}\n{boid.p1.x:,.2f}, {boid.p1.y:,.2f}\n{boid.p2.x:,.2f}, {boid.p2.y:,.2f}\n{boid.p3.x:,.2f}, {boid.p3.y:,.2f}\n"
    #             f.write(s)
    #             f.write(f"al:{boid.alignment}")
    #     else:
    #         with open("pos.txt", "a") as f:
    #             f.write(f"\n")
    #             s = f"{boid.center.x:,.2f}, {boid.center.y:,.2f}\n{boid.p1.x:,.2f}, {boid.p1.y:,.2f}\n{boid.p2.x:,.2f}, {boid.p2.y:,.2f}\n{boid.p3.x:,.2f}, {boid.p3.y:,.2f}\n"
    #             f.write(s)
    #             f.write(f"al:{boid.alignment}")
    #     Boid._itercount += 1
