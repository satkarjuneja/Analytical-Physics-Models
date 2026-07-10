# This script calculates the most stable configuration for 108 water molecules
# particles start off in a random state
# then move towards the more stable state using Gradient Descent


import numpy as np
import matplotlib.pyplot as plt

def LeonardJones(R):
    return 4 * ((3.4 / R)**12 - (3.4 / R)**6)

def force(R):
    return 4 * ep * ((3.4**12) * (-12) / (R**13) + (3.4**6) * (6) / (R**7))

def dis(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)


x_data = []
y_data = []
z_data = []
num = 108
size = 18.5
radius = 1.7

while len(x_data) < num:
    cx, cy, cz = np.random.uniform(-size + radius, size - radius, 3)
    if x_data:
        distances=dis(np.array(x_data),np.array(y_data),np.array(z_data),cx,cy,cz)
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
α = 0.002
distance = np.zeros((num, num))

U = 0
for i in range(num):
    for j in range(i + 1, num):
        R = dis(x_data[i],y_data[i],z_data[i],x_data[j],y_data[j],z_data,[j])
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
                R = dis(x_data[i],y_data[i],z_data[i],x_data[j],y_data[j],z_data,[j])
                p += force(R)
        Upar.append(p)

    forcex, forcey, forcez = [], [], []
    for i in range(num):
        x, y, z = 0, 0, 0
        for j in range(num):
            if i != j:
                R = dis(x_data[i],y_data[i],z_data[i],x_data[j],y_data[j],z_data,[j])
                if R != 0:
                    x += -Upar[i] * (x_data[i] - x_data[j]) / R
                    y += -Upar[i] * (y_data[i] - y_data[j]) / R
                    z += -Upar[i] * (z_data[i] - z_data[j]) / R
        forcex.append(x)
        forcey.append(y)
        forcez.append(z)

    for i in range(num):
        x_data[i] += α * forcex[i]
        y_data[i] += α * forcey[i]
        z_data[i] += α * forcez[i]

    U_current = 0
    for i in range(num):
        for j in range(i + 1, num):
            R = dis(x_data[i],y_data[i],z_data[i],x_data[j],y_data[j],z_data,[j])
            U_current += LeonardJones(R)

    Utime.append(U_current)

    if U_current > previous_U * 2:
        print(f"[Warning] k={k}: Potential spiked from {previous_U:.5f} to {U_current:.5f}")

    previous_U = U_current

    if k % 5 == 0: # plot every 5 steps to prevent overload
        ax.cla()
        ax.scatter(x_data, y_data, z_data, s=5)
        ax.text(0, 25, 25, f"U = {U_current:.6f}", color='red')
        plt.draw()
        plt.pause(0.001)

plt.ioff()
plt.show()
