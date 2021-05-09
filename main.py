import tkinter as tk

from boid import Boid

height = 600
width = 800
bgc = "#292841"
boid_count = 100


class App(object):
    # boids = []

    def __init__(self, app_root):
        self.root = app_root
        self.toolbar = tk.Frame(self.root, height=30, width=width)
        self.init_toolbar(self.toolbar)
        self.b_apply = tk.Button(self.toolbar, text="Apply", width=5)
        self.b_apply.grid(row=0, column=8, padx=5)
        self.b_run = tk.Button(self.toolbar, text="Run", width=5, command=self.run_click)
        self.b_run.grid(row=0, column=9, padx=5)
        self.toolbar.pack()
        self.cnv = tk.Canvas(self.root, bg=bgc, height=height, width=width)
        self.cnv.pack()
        self.boids = []

    def run_click(self):
        if self.b_run["text"] == "Run":
            self.b_run["text"] = "Stop"
            self.boids = App._init_boids(self.cnv, boid_count, width, height)
            self.root.after(0, self._animation())
        else:
            self.b_run["text"] = "Run"
            # todo figure out how to actually stop the animation
            self.cnv.delete("all")
            self.boids = []

    @staticmethod
    def init_toolbar(toolbar):
        App._init_count(toolbar)
        App._init_speed(toolbar)
        App._init_viewdist(toolbar)
        App._init_sepdist(toolbar)

    @staticmethod
    def _init_sepdist(toolbar):
        l_sep = tk.Label(toolbar, text="Separation distance:")
        l_sep.grid(row=0, column=6, padx=5)
        in_sep = tk.Scale(toolbar, from_=10, to=500, width=10, orient=tk.HORIZONTAL)
        in_sep.set(50)
        in_sep.grid(row=0, column=7, padx=5)

    @staticmethod
    def _init_viewdist(toolbar):
        l_view = tk.Label(toolbar, text="View distance:")
        l_view.grid(row=0, column=4, padx=5)
        in_view = tk.Scale(toolbar, from_=10, to=500, width=10, orient=tk.HORIZONTAL)
        in_view.set(100)
        in_view.grid(row=0, column=5, padx=5)

    @staticmethod
    def _init_speed(toolbar):
        l_speed = tk.Label(toolbar, text="Speed:")
        l_speed.grid(row=0, column=2, padx=5)
        in_speed = tk.Scale(toolbar, from_=1, to=50, width=10, orient=tk.HORIZONTAL)
        in_speed.set(10)
        in_speed.grid(row=0, column=3, padx=5)

    @staticmethod
    def _init_count(toolbar):
        l_count = tk.Label(toolbar, text="Count:")
        l_count.grid(row=0, column=0, padx=5)
        in_count = tk.Entry(toolbar, width=5)
        in_count.grid(row=0, column=1, padx=5)
        in_count.insert(0, '100')

    def _animation(self):
        self.root.update()
        for boid in self.boids:
            boid.move()
        self.root.after(100, self._animation)

    @staticmethod
    def _init_boids(canvas, count, c_width, c_height):
        boids = []
        for i in range(count):
            boids.append(Boid.init_rand_boid(canvas, c_width, c_height))
        return boids


root = tk.Tk()
root.title("boids")
root.iconbitmap("resources/boids.ico")
app = App(root)
root.mainloop()
