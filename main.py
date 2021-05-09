import tkinter as tk

from boid import Boid


class App(object):
    _animation = None
    _boid_count = 100
    _height = 600
    _width = 800
    _bgc = "#292841"
    _boids = []
    _frame_length = 100

    def __init__(self, app_root):
        self.root = app_root
        self.toolbar = tk.Frame(self.root, height=30, width=App._width)
        self._init_labels(self.toolbar)

        self.in_count = tk.Entry(self.toolbar, width=5)
        self.in_count.grid(row=0, column=1, padx=5)
        self.in_count.insert(0, App._boid_count)

        self.in_speed = tk.Scale(self.toolbar, from_=1, to=50, width=10, orient=tk.HORIZONTAL)
        self.in_speed.set(Boid.speed)
        self.in_speed.grid(row=0, column=3, padx=5)

        self.in_view = tk.Scale(self.toolbar, from_=10, to=500, width=10, orient=tk.HORIZONTAL)
        self.in_view.set(Boid.view_dist)
        self.in_view.grid(row=0, column=5, padx=5)

        self.in_sep = tk.Scale(self.toolbar, from_=10, to=500, width=10, orient=tk.HORIZONTAL)
        self.in_sep.set(Boid.sep_dist)
        self.in_sep.grid(row=0, column=7, padx=5)

        self.b_run = tk.Button(self.toolbar, text="Run", width=5, command=self._run_click)
        self.b_run.grid(row=0, column=8, padx=5)

        self.toolbar.pack()
        self.cnv = tk.Canvas(self.root, bg=App._bgc, height=App._height, width=App._width)
        self.cnv.pack()

    def _animate(self):
        self.root.update()
        for boid in self._boids:
            boid.move()
        App._animation = self.root.after(App._frame_length, self._animate)

    def _boids_start(self):
        App._boid_count = int(self.in_count.get())
        Boid.speed = int(self.in_speed.get())
        Boid.view_dist = int(self.in_view.get())
        Boid.sep_dist = int(self.in_sep.get())
        self._boids = App._init_boids(self.cnv, App._boid_count, App._width, App._height)
        self._animate()

    def _boids_stop(self):
        self.root.after_cancel(App._animation)
        App._animation = None
        self.cnv.delete("all")
        self._boids = []

    def _run_click(self):
        if self.b_run["text"] == "Run":
            self.b_run["text"] = "Stop"
            self.in_count.configure(state=tk.DISABLED)
            self.in_speed.configure(state=tk.DISABLED)
            self.in_view.configure(state=tk.DISABLED)
            self.in_sep.configure(state=tk.DISABLED)
            self._boids_start()
        else:
            self.b_run["text"] = "Run"
            self.in_count.configure(state=tk.NORMAL)
            self.in_speed.configure(state=tk.ACTIVE)
            self.in_view.configure(state=tk.ACTIVE)
            self.in_sep.configure(state=tk.ACTIVE)
            self._boids_stop()

    @staticmethod
    def _init_labels(toolbar):
        l_count = tk.Label(toolbar, text="Count:")
        l_speed = tk.Label(toolbar, text="Speed:")
        l_view = tk.Label(toolbar, text="View distance:")
        l_sep = tk.Label(toolbar, text="Separation distance:")
        l_count.grid(row=0, column=0, padx=5)
        l_speed.grid(row=0, column=2, padx=5)
        l_view.grid(row=0, column=4, padx=5)
        l_sep.grid(row=0, column=6, padx=5)

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
