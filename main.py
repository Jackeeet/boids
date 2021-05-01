import tkinter as tk

from boid import Boid

height = 600
width = 800
bgc = "#292841"
boid_count = 10


class App(object):
    def __init__(self, app_root):
        self.root = app_root
        self.root.title("boids")
        self.cnv = tk.Canvas(self.root, bg=bgc, height=height, width=width)
        self.cnv.pack()
        self.boids = self.init_boids(boid_count, width, height)
        self.cnv.pack()
        self.root.after(0, self.animation)

    def animation(self):
        self.root.update()
        for boid in self.boids:
            boid.move()
        self.root.after(12, self.animation)

    def init_boids(self, count, c_width, c_height):
        boids = []
        for i in range(count):
            boids.append(Boid.init_rand_boid(self.cnv, c_width, c_height))
        return boids


root = tk.Tk()
app = App(root)
root.mainloop()
