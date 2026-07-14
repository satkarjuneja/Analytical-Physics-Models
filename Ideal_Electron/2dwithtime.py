import numpy as np
import matplotlib.pyplot as plt
import random

x_data = []
y_data = []
t_data = []

steps = 10000

position = [0, 0, 0]

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
lx = 0
ly = 0
lt = 0
for i in range(0, steps):
    axes = random.choice([0, 1])
    if axes == 0:
        step = random.choice([-1, 1])
        lx = lx + step
        position.append([lx, ly, i])

    elif axes == 1:
        step = random.choice([-1, 1])
        ly = ly + step
        position.append([lx, ly, i])
        # x_data.append(0)
        # y_data.append(ly)
        # z_data.append(0)
    x_data.append(lx)
    y_data.append(ly)
    t_data.append(lt)
    ax.plot(x_data, y_data, t_data, marker="o", color="black")
    ax.set_box_aspect([1, 1, 1])
    plt.pause(0.05)


ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Plot Example")
ax.legend()
ax.scatter(
    x_data[-1],
    y_data[-1],
    t_data[-1],
    color="red",
)
ax.set_xlim(-5000, 5000)
ax.set_ylim(-5000, 5000)
ax.set_zlim(-5000, 5000)


plt.show()
