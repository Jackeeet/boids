import random
import tkinter as tk
from math import cos, sin, atan2, pi

height = 600
width = 800
bgc = "#292841"
boid_count = 1


def sign(point, l_start, l_end):
    return (point[0] - l_end[0]) * (l_start[1] - l_end[1]) - (l_start[0] - l_end[0]) * (point[1] - l_end[1])


def point_in_sector(point, sector):
    x1, y1, x2, y2, x3, y3 = sector
    s1 = sign(point, (x1, y1), (x2, y2))
    s2 = sign(point, (x2, y2), (x3, y3))
    s3 = sign(point, (x3, y3), (x1, y1))
    negative = (s1 < 0) or (s2 < 0) or (s3 < 0)
    positive = (s1 > 0) or (s2 > 0) or (s3 > 0)
    return not (negative and positive)


class Boid(object):
    speed = 2
    size = (10, 24)
    colour = "white"
    view_dist = 50
    view_angle = 5 * pi / 6
    sep_dist = 24

    def __init__(self, cnv, rotation=0.0, *points, **kwargs):
        self.cnv = cnv
        self.id = cnv.create_polygon(*points, **kwargs)
        self.p1 = (points[0], points[1])
        self.p2 = (points[2], points[3])
        self.p3 = (points[4], points[5])
        self.center = self.get_center(*points)
        self.alignment = rotation
        self.dx = self.speed
        self.dy = self.speed

    @classmethod
    def get_rand_boid(cls, canvas):
        r = random.uniform(0.0, 2 * pi)
        xc = random.randint(0, width)
        yc = random.randint(0, height)
        x1 = xc + cls.size[0] / 2 * cos(pi / 2 + r)
        y1 = yc - cls.size[0] / 2 * sin(pi / 2 + r)
        x2 = xc + cls.size[0] / 2 * cos(-pi / 2 + r)
        y2 = yc - cls.size[0] / 2 * sin(-pi / 2 + r)
        x3 = xc + cls.size[1] * cos(r)
        y3 = yc - cls.size[1] * sin(r)
        return Boid(canvas, r, x1, y1, x2, y2, x3, y3, fill=cls.colour)

    @staticmethod
    def get_center(*points):
        return 1 / 3 * sum(points[::2]), 1 / 3 * sum(points[1::2])

    def update_coords(self):
        x0, y0 = self.p1
        x1, y1 = self.p2
        x2, y2 = self.p3
        self.center = self.get_center(x0, y0, x1, y1, x2, y2)
        self.cnv.coords(self.id, x0, y0, x1, y1, x2, y2)

    def get_um_sector(self, xc, yc):
        xs = xc + type(self).view_dist * cos(type(self).view_angle / 2)
        ys = yc - type(self).view_dist * sin(type(self).view_angle / 2)
        xe = xc + type(self).view_dist * cos(-type(self).view_angle / 2)
        ye = yc - type(self).view_dist * sin(-type(self).view_angle / 2)
        return xs, ys, xc, yc, xe, ye

    def rotate(self, angle):
        xc, yc = self.center
        self.alignment += angle
        self.p1 = (xc + type(self).size[0] / 2 * cos(pi / 2 + angle),
                   yc - type(self).size[0] / 2 * sin(pi / 2 + angle))
        self.p2 = (xc + type(self).size[0] / 2 * cos(-pi / 2 + angle),
                   yc - type(self).size[0] / 2 * sin(-pi / 2 + angle))
        self.p3 = (xc + type(self).size[1] * cos(angle),
                   yc - type(self).size[1] * sin(angle))
        self.update_coords()

    def align(self):
        pass

    def move(self):
        x1 = self.p1[0] + self.dx
        y1 = self.p1[1] + self.dy
        x2 = self.p2[0] + self.dx
        y2 = self.p2[1] + self.dy
        x3 = self.p3[0] + self.dx
        y3 = self.p3[1] + self.dy

        if x3 >= width:
            x1 = -type(self).size[1]
            x2 = -type(self).size[1]
            x3 = 0
        elif x3 <= 0:
            x1 = width + type(self).size[1]
            x2 = width + type(self).size[1]
            x3 = width

        if y3 >= height:
            y1 = -type(self).size[1]
            y2 = -type(self).size[1]
            y3 = 0
        elif y3 <= 0:
            y1 = height + type(self).size[1]
            y2 = height + type(self).size[1]
            y3 = height

        self.p1 = x1, y1
        self.p2 = x2, y2
        self.p3 = x3, y3
        self.update_coords()


class App(object):
    def __init__(self, root, **kwargs):
        self.root = root
        self.root.title("boids")
        self.cnv = tk.Canvas(self.root, bg=bgc, height=height, width=width)
        self.cnv.pack()
        self.boids = self.init_boids(boid_count)
        self.cnv.pack()
        self.root.after(0, self.animation)

    def animation(self):
        for boid in self.boids:
            boid.move()
        self.root.after(12, self.animation)

    def init_boids(self, count):
        boids = []
        for i in range(count):
            boids.append(Boid.get_rand_boid(self.cnv))
        return boids


root = tk.Tk()
app = App(root)
root.mainloop()

# x1, y1, x2, y2 = self.cnv.bbox(self.id)
# if x1 < 0 or x2 > width:
#     self.dx *= -1
# if y1 < 0 or y2 > height:
#     self.dy *= -1
# self.cnv.move(self.id, self.dx, self.dy)


# tx = 0
# if x < 0:
#     tx = width
# elif x > width:
#     tx = -width
# ty = 0
# if y < 0:
#     ty = y + height
# elif y > height:
#     ty = y - height
#
# if tx == 0 and ty == 0:
#     self.cnv.move(self.id, self.dx, self.dy)
# elif tx != 0 and ty != 0:
#     self.cnv.move(self.id, tx, ty)
# elif ty == 0:
#     self.cnv.move(self.id, tx, self.dy)
# else:
#     self.cnv.move(self.id, self.dx, ty)
