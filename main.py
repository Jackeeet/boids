import random
import tkinter as tk
from math import cos, sin, atan2, pi

height = 600
width = 800
bgc = "#292841"
boid_count = 1


# boid_size = (8, 10)
# boid_speed = 5


class Boid(object):
    size = (8, 10)
    speed = 5
    beak_len = 1

    def __init__(self, cnv, x, y, rotation=0.0, **kwargs):
        self.pos = x, y
        self.cnv = cnv
        x1, y1, x2, y2 = self.get_box(x, y, self.size)
        self.id = cnv.create_oval(x1, y1, x2, y2, tags=f"b{id(self)}", **kwargs)
        self.rotation = rotation
        self.dx = self.speed
        self.dy = self.speed
        self.beak = cnv.create_line(self.pos[0], self.pos[1],
                                    self.beak_len * cos(self.rotation),
                                    self.beak_len * sin(self.rotation),
                                    tags=f"b{id(self)}",fill="white")

    @staticmethod
    def get_box(x, y, size):
        x1 = x - size[0] / 2
        y1 = y - size[1] / 2
        x2 = x + size[0] / 2
        y2 = y + size[1] / 2
        return x1, y1, x2, y2

    def move(self):
        x1, y1, x2, y2 = self.cnv.bbox(self.id)
        if x1 < 0 or x2 > width:
            self.dx *= -1
        if y1 < 0 or y2 > height:
            self.dy *= -1
        self.cnv.move(f"b{id(self)}", self.dx, self.dy)


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
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.random()
            boids.append(Boid(self.cnv, x, y, r, fill='white'))
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
