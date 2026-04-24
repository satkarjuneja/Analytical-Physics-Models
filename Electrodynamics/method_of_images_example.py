import numpy as np
import matplotlib.pyplot as plt

k = 1

def V_total(q1, q2, x, y, z, d):
    r1 = np.sqrt(x**2 + y**2 + z**2)
    r2 = np.sqrt((x - d)**2 + y**2 + z**2)
    return k * (q1 / r1 + q2 / r2)

def generate_3d(q1, q2, d):
    x = np.linspace(-2, 3*d, 200)
    y = np.linspace(-2, 3*d, 200)
    z = np.linspace(-2, 3*d, 200)

    X, Y, Z = np.meshgrid(x, y, z)

    r1 = np.sqrt(X**2 + Y**2 + Z**2)
    r2 = np.sqrt((X - d)**2 + Y**2 + Z**2)

    eps = 1e-3
    valid = (r1 > eps) & (r2 > eps)

    V = np.zeros_like(X)
    V[valid] = k * (q1 / r1[valid] + q2 / r2[valid])
    V[~valid] = np.nan

    return V, X, Y, Z

def run_matplotlib_3d(q1, q2, d):
    V, X, Y, Z = generate_3d(q1, q2, d)

    mask = np.isclose(V, 0, atol=1e-2)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(X[mask], Y[mask], Z[mask], s=1)

    ax.scatter([0, d], [0, 0], [0, 0], color='black', s=50)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.show()

run_matplotlib_3d(1, -0.5, 4)