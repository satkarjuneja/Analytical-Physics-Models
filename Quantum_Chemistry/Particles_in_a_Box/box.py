import numpy as np
import matplotlib.pyplot as plt
import random

# Helper Functions

def distance(x1, y1, z1, x2, y2, z2):
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5

def lj_potential(r, sigma=3.4, epsilon=1.0):
    return 4 * epsilon * ((sigma/r)**12 - (sigma/r)**6)

def numerical_derivative(f, x, dx=1e-6):
    return (f(x + dx) - f(x)) / dx

# Setup

x_data, y_data, z_data = [], [], []
num  = 108   # 108 because the first ever computational model used 108 molecules :)
size = 18.5  # Size of Box
radius = 1.7 # Radius of Atom

while len(x_data) < num:
    cx, cy, cz = np.random.uniform(-size + radius, size - radius, 3)
    if x_data:
        distances = distance(np.array(x_data), np.array(y_data), np.array(z_data), cx, cy, cz)
        if np.all(distances >= 2 * radius):
            x_data.append(cx); y_data.append(cy); z_data.append(cz)
    else:
        x_data.append(cx); y_data.append(cy); z_data.append(cz)

x_data = np.array(x_data)
y_data = np.array(y_data)
z_data = np.array(z_data)

#Potential Energy Calculation 

U = 0
U_data = []
xi = 2  # reference particle index

for i in range(num):
    for j in range(i+1, num):
        R = distance(x_data[i], y_data[i], z_data[i], x_data[j], y_data[j], z_data[j])
        if R > 3.4:
            U = lj_potential(R)
            U_data.append(U)

#Force on reference particle (x-component)

for i in range(num):
    if i != xi:
        def f(x):
            return distance(x, y_data[xi], z_data[xi], x_data[i], y_data[i], z_data[i])
        df = numerical_derivative(f, x_data[xi])

print("U =", U)
print("Fx1 =", df)

#Plot Initial Configuration 

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_data, y_data, z_data, s=5)
plt.show()