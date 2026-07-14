import numpy as np
import matplotlib.pyplot as plt
import random

x_data = []
y_data = []
z_data = []

x2_data = []
y2_data = []
z2_data = []


steps = 10000

position = [0, 0, 0]
position2 = [0, 0, 0]
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
lx = 0
ly = 0
lz = 0
lx2 = 0
ly2 = 0
lz2 = 0
for i in range(0, steps):
    axes = random.choice([0, 1, 2])
    if axes == 0:
        step = random.choice([-1, 1])
        lx = lx + step
        position.append([lx, ly, lz])

    elif axes == 1:
        step = random.choice([-1, 1])
        ly = ly + step
        position.append([lx, ly, lz])
        # x_data.append(0)
        # y_data.append(ly)
        # z_data.append(0)
    else:
        step = random.choice([-1, 1])
        lz = lz + step
        # x_data.append(0)
        # y_data.append(0)
        # z_data.append(lz)
        position.append([lx, ly, lz])
    axes2 = random.choice([0, 1, 2])
    if axes2 == 0:
        step2 = random.choice([-1, 1])
        lx2 = lx2 + step2
        position.append([lx2, ly2, lz2])

    elif axes2 == 1:
        step2 = random.choice([-1, 1])
        ly2 = ly2 + step2
        position.append([lx2, ly2, lz2])
        # x_data.append(0)
        # y_data.append(ly)
        # z_data.append(0)
    else:
        step2 = random.choice([-1, 1])
        lz2 = lz2 + step2
        # x_data.append(0)
        # y_data.append(0)
        # z_data.append(lz)
        position.append([lx2, ly2, lz2])
    x_data.append(lx)
    y_data.append(ly)
    z_data.append(lz)
    x2_data.append(lx2)
    y2_data.append(ly2)
    z2_data.append(lz2)
    ax.plot(x_data, y_data, z_data, marker="o", color="black")
    ax.plot(x2_data, y2_data, z2_data, marker="o", color="blue")

    ax.set_box_aspect([2, 2, 2])
    plt.pause(0.05)


ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("3D Plot Example")
ax.legend()
ax.scatter(
    x_data[-1],
    y_data[-1],
    z_data[-1],
    color="red",
)
ax.set_xlim(-5000, 5000)
ax.set_ylim(-5000, 5000)
ax.set_zlim(-5000, 5000)


plt.show()
