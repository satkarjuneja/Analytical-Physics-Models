from manim import *
import numpy as np
from scipy.ndimage import laplace
import matplotlib.pyplot as plt
Du = 0.16   # diffusion rate of u
Dv = 0.08   # diffusion rate of v
F = 0.055   # feed rate
k = 0.062   # kill rate
N = 450     # grid size
dt = 1.0    # timestep
steps_per_frame = 20
n_frames = 1000

def init_grid(N):
    u = np.ones((N, N))
    v = np.zeros((N, N))
    r = 10
    c = N // 2
    u[c-r:c+r, c-r:c+r] = 0.50
    v[c-r:c+r, c-r:c+r] = 0.25
    u += 0.02 * np.random.random((N, N))
    v += 0.02 * np.random.random((N, N))
    return u, v

def step(u, v):
    lu = laplace(u, mode='wrap')
    lv = laplace(v, mode='wrap')
    uvv = u * v * v
    du = Du * lu - uvv + F * (1 - u)
    dv = Dv * lv + uvv - (F + k) * v
    return u + dt * du, v + dt * dv

def v_to_rgb(v):
    norm = (v - v.min()) / (v.max() - v.min() + 1e-9)
    cmap = plt.get_cmap('viridis')
    rgba = cmap(norm)
    rgb = (rgba[:, :, :3] * 255).astype(np.uint8)
    return rgb

class Visual(Scene):
    def construct(self):
        title = Text("Gray-Scott Reaction-Diffusion System", font_size=32)
        title.to_edge(UP, buff=0.4)
        self.add(title)

        u, v = init_grid(N)

        frames = []
        for _ in range(n_frames):
            for _ in range(steps_per_frame):
                u, v = step(u, v)
            frames.append(v_to_rgb(v))

        img = ImageMobject(frames[0])
        img.scale_to_fit_height(5.5)
        img.next_to(title, DOWN, buff=0.5)
        self.add(img)

        for frame in frames[1:]:
            new_img = ImageMobject(frame)
            new_img.scale_to_fit_height(5.5)
            new_img.move_to(img)
            img.become(new_img)
            self.wait(1/30)