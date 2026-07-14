import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

M = 100000
N = 100
bin_width = 1


steps = np.random.choice([-1, 1], size=(M, N, 2))

final_positions = steps.sum(axis=1)
xf = final_positions[:, 0]
yf = final_positions[:, 1]


max_range = int(max(np.abs(xf).max(), np.abs(yf).max())) + 1
edges = np.arange(-max_range - 0.5, max_range + 0.6, bin_width)


H, xedges, yedges = np.histogram2d(xf, yf, bins=[edges, edges])


xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = np.zeros_like(xpos)


dx = dy = (xedges[1] - xedges[0]) * 0.8
dz = H.ravel()


fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, shade=True)

ax.set_xlabel("X position")
ax.set_ylabel("Y position")
ax.set_zlabel("Number of walks ending here")
plt.show()
