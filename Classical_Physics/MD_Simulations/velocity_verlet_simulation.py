import numpy as np
import matplotlib.pyplot as plt

sigma = 1
epsilon = 1  # Arbitrary units
BURN_IN = 2000


def distance(x1, y1, z1, x2, y2, z2):
    """Gives the euclidian distance between 2 points in space
    input: (x1,y1,z1,x2,y2,z2)
    """
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2) ** 0.5


def leonard_jones(r):
    """Return potential according to leonard jones potential funtion
    input: r(distance bewteen 2 particles)
    """
    return 4 * epsilon * ((sigma / r) ** 12 - (sigma / r) ** 6)


def calculate_energy(X, Y, Z):
    dx = X[:, None] - X[None, :]  # N×N displacement matrices
    dy = Y[:, None] - Y[None, :]
    dz = Z[:, None] - Z[None, :]

    r = np.sqrt(dx**2 + dy**2 + dz**2)
    np.fill_diagonal(r, np.inf)  # ignore self-interaction
    u = 0
    u += np.sum(leonard_jones(r)) / 2  # prevent double counting
    return u


def force(X, Y, Z):
    dx = X[:, None] - X[None, :]  # N×N displacement matrices
    dy = Y[:, None] - Y[None, :]
    dz = Z[:, None] - Z[None, :]

    r2 = dx**2 + dy**2 + dz**2
    np.fill_diagonal(r2, np.inf)  # ignore self-interaction

    f = 24 * epsilon * (2 * sigma**12 / r2**7 - sigma**6 / r2**4)
    np.fill_diagonal(f, 0)  # force on self is zero

    Fx = np.sum(f * dx, axis=1)
    Fy = np.sum(f * dy, axis=1)
    Fz = np.sum(f * dz, axis=1)

    return np.column_stack([Fx, Fy, Fz])


def generate(N, steps, delta_t, L, m):
    avg_V = []
    avg_E = []
    sample_pos = []
    time = []

    X, Y, Z = [], [], []

    Vx = np.random.uniform(-1, 1, size=N)
    Vy = np.random.uniform(-1, 1, size=N)
    Vz = np.random.uniform(-1, 1, size=N)

    Vx -= np.mean(Vx)
    Vy -= np.mean(Vy)
    Vz -= np.mean(Vz)

    r_min = 2 ** (1 / 6) * sigma  # LJ equilibrium distance, ~1.12

    while len(X) < N:
        x = np.random.uniform(-L, L)
        y = np.random.uniform(-L, L)
        z = np.random.uniform(-L, L)

        ok = True
        for i in range(len(X)):
            dx = x - X[i]
            dy = y - Y[i]
            dz = z - Z[i]
            r = np.sqrt(dx * dx + dy * dy + dz * dz)

            if r < r_min:
                ok = False
                break

        if ok:
            X.append(x)
            Y.append(y)
            Z.append(z)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)

    X_ini = X.copy()
    Y_ini = Y.copy()
    Z_ini = Z.copy()

    F = force(X, Y, Z)

    # initial potential energy

    U = calculate_energy(X, Y, Z)

    for ti in range(
        steps * N * N
    ):  # Monte Carlo Steps (one run steps is equal to 1 montecarlo step)
        ax = F[:, 0] / m
        ay = F[:, 1] / m
        az = F[:, 2] / m

        # position
        X = X + Vx * delta_t + 0.5 * ax * (delta_t**2)
        Y = Y + Vy * delta_t + 0.5 * ay * (delta_t**2)
        Z = Z + Vz * delta_t + 0.5 * az * (delta_t**2)

        # Reflection of particles from the walls
        # X walls
        maskx = X > L
        X[maskx] = 2 * L - X[maskx]
        Vx[maskx] = -Vx[maskx]

        maskx2 = X < -L
        X[maskx2] = -2 * L - X[maskx2]
        Vx[maskx2] = -Vx[maskx2]

        # Y walls
        masky = Y > L
        Y[masky] = 2 * L - Y[masky]
        Vy[masky] = -Vy[masky]

        masky2 = Y < -L
        Y[masky2] = -2 * L - Y[masky2]
        Vy[masky2] = -Vy[masky2]

        # Z walls
        maskz = Z > L
        Z[maskz] = 2 * L - Z[maskz]
        Vz[maskz] = -Vz[maskz]

        maskz2 = Z < -L
        Z[maskz2] = -2 * L - Z[maskz2]
        Vz[maskz2] = -Vz[maskz2]

        # recalculate forces
        F_new = force(X, Y, Z)

        ax_new = F_new[:, 0] / m
        ay_new = F_new[:, 1] / m
        az_new = F_new[:, 2] / m

        # velocity update
        Vx = Vx + 0.5 * (ax + ax_new) * delta_t
        Vy = Vy + 0.5 * (ay + ay_new) * delta_t
        Vz = Vz + 0.5 * (az + az_new) * delta_t

        F = F_new

        U = calculate_energy(X, Y, Z)

        K = 0.5 * m * np.sum(Vx**2 + Vy**2 + Vz**2)

        avg_E.append(K + U)

        v_mag = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        avg_V.append(np.mean(v_mag))

        sample_pos.append(np.sqrt(X[0] ** 2 + Y[0] ** 2 + Z[0] ** 2))

        time.append(ti)
        print(f"Step: {ti}", end="\r")

    print(f"Initial Energy: {avg_E[0]}")
    print(f"Final Energy: {avg_E[-1]}")

    return X_ini, Y_ini, Z_ini, X, Y, Z, sample_pos, avg_E, avg_V, time


def run_matplotlib(N, steps, delta_t, L, m):
    X_ini, Y_ini, Z_ini, X, Y, Z, avg_pos, avg_E, avg_V, time = generate(
        N, steps, delta_t, L, m
    )

    fig = plt.figure(figsize=(12, 8))

    ax1 = fig.add_subplot(231, projection="3d")
    ax1.scatter(X_ini, Y_ini, Z_ini)
    ax1.set_title("Initial")

    ax2 = fig.add_subplot(232, projection="3d")
    ax2.scatter(X, Y, Z)
    ax2.set_title("Final")

    ax3 = fig.add_subplot(233)
    ax3.plot(time[BURN_IN:], avg_pos[BURN_IN:])
    ax3.grid()
    ax3.set_title("Sample Position vs Time")

    ax4 = fig.add_subplot(234)
    ax4.plot(time[BURN_IN:], avg_V[BURN_IN:])
    ax4.grid()
    ax4.set_title("Avg Velocity vs Time")

    ax5 = fig.add_subplot(235)
    ax5.plot(time[BURN_IN:], avg_E[BURN_IN:])
    ax5.grid()
    ax5.set_title("Total Energy vs Time")

    plt.tight_layout()
    plt.show()


# n,steps,time,L,m
run_matplotlib(10, 300, 0.0001, 3, 1)
