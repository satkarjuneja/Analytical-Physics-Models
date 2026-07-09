import numpy as np
import matplotlib.pyplot as plt
import random


def LeonardJones(R):
    return 4 * ((3.4 / R)**12 - (3.4 / R)**6)


x_data = []
y_data = []
z_data = []
num = 108
size = 18.5
radius = 1.7

while len(x_data) < num:
    cx, cy, cz = np.random.uniform(-size + radius, size - radius, 3)
    if x_data:
        distances = np.sqrt((np.array(x_data) - cx)**2 +
                            (np.array(y_data) - cy)**2 +
                            (np.array(z_data) - cz)**2)
        if np.all(distances >= 2 * radius):
            x_data.append(cx)
            y_data.append(cy)
            z_data.append(cz)
    else:
        x_data.append(cx)
        y_data.append(cy)
        z_data.append(cz)

x_data = np.array(x_data)
y_data = np.array(y_data)
z_data = np.array(z_data)

ep = 0.238
alp = 0.002
distance = np.zeros((num, num))

U = 0
for i in range(num):
    for j in range(i + 1, num):
        R = np.sqrt((x_data[i] - x_data[j])**2 +
                    (y_data[i] - y_data[j])**2 +
                    (z_data[i] - z_data[j])**2)
        distance[i, j] = R
        distance[j, i] = R
        U += LeonardJones(R)

Utime = [U]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
plt.ion()

previous_U = U

for k in range(1000):
    Upar = []
    for i in range(num):
        p = 0
        for j in range(num):
            if i != j:
                R = np.sqrt((x_data[i] - x_data[j])**2 +
                            (y_data[i] - y_data[j])**2 +
                            (z_data[i] - z_data[j])**2)
                p += 4 * ep * ((3.4**12) * (-12) / (R**13) + (3.4**6) * (6) / (R**7))
        Upar.append(p)

    forcex, forcey, forcez = [], [], []
    for i in range(num):
        x, y, z = 0, 0, 0
        for j in range(num):
            if i != j:
                R = np.sqrt((x_data[i] - x_data[j])**2 +
                            (y_data[i] - y_data[j])**2 +
                            (z_data[i] - z_data[j])**2)
                if R != 0:
                    x += -Upar[i] * (x_data[i] - x_data[j]) / R
                    y += -Upar[i] * (y_data[i] - y_data[j]) / R
                    z += -Upar[i] * (z_data[i] - z_data[j]) / R
        forcex.append(x)
        forcey.append(y)
        forcez.append(z)

    for i in range(num):
        x_data[i] += alp * forcex[i]
        y_data[i] += alp * forcey[i]
        z_data[i] += alp * forcez[i]

    U_current = 0
    for i in range(num):
        for j in range(i + 1, num):
            R = np.sqrt((x_data[i] - x_data[j])**2 +
                        (y_data[i] - y_data[j])**2 +
                        (z_data[i] - z_data[j])**2)
            U_current += LeonardJones(R)

    Utime.append(U_current)

    if U_current > previous_U * 2:
        print(f"[Warning] k={k}: Potential spiked from {previous_U:.5f} to {U_current:.5f}")

    previous_U = U_current

    if k % 5 == 0:
        ax.cla()
        ax.scatter(x_data, y_data, z_data, s=5)
        ax.text(0, 25, 25, f"U = {U_current:.6f}", color='red')
        plt.draw()
        plt.pause(0.001)

plt.ioff()
plt.show()
