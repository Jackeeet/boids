import random
import tkinter as tk
from math import cos, sin, atan2, pi

height = 600
width = 800
bgc = "#292841"
boid_count = 100
boid_size = (10, 24)


class Boid(object):
    speed = 5

    def __init__(self, cnv, rotation=0.0, *points, **kwargs):
        self.cnv = cnv
        self.id = cnv.create_polygon(*points, **kwargs)
        self.pos = self.get_center(*points)
        self.rotation = rotation
        self.dx = self.speed
        self.dy = self.speed

    @staticmethod
    def get_center(*points):
        return 1 / 3 * sum(points[::2]), 1 / 3 * sum(points[1::2])

    def move(self):
        x1, y1, x2, y2 = self.cnv.bbox(self.id)
        if x1 < 0 or x2 > width:
            self.dx *= -1
        if y1 < 0 or y2 > height:
            self.dy *= -1
        self.cnv.move(self.id, self.dx, self.dy)


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
            r = random.uniform(0.0, 2 * pi)
            xc = random.randint(0, width)
            yc = random.randint(0, height)
            x1 = xc + boid_size[0] / 2 * cos(pi / 2 + r)
            y1 = yc - boid_size[0] / 2 * sin(pi / 2 + r)
            x2 = xc + boid_size[0] / 2 * cos(-pi / 2 + r)
            y2 = yc - boid_size[0] / 2 * sin(-pi / 2 + r)
            x3 = xc + boid_size[1] * cos(r)
            y3 = yc - boid_size[1] * sin(r)
            boids.append(Boid(self.cnv, r, x1, y1, x2, y2, x3, y3, fill='white'))
        return boids


root = tk.Tk()
app = App(root)
root.mainloop()

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
