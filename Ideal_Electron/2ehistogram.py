import numpy as np
import matplotlib.pyplot as plt

walks1 = 100000
num_steps = 5000
walks2 = 100000
num_steps2 = 5000

final_positions1 = []
final_positions2 = []
arr = []
for _ in range(walks1):
    steps1 = np.random.choice([-1, 1], size=num_steps)
    steps2 = np.random.choice([-1, 1], size=num_steps2)
    position = np.sum(steps1)
    position2 = np.sum(steps2)
    if position == position2:
        arr.append(position)
        position = 0
        position2 = 0

arr = np.array(arr)
min_pos = arr.min()
max_pos = arr.max()
bins = np.arange(min_pos - 0.5, max_pos + 0.5, 1)

plt.figure(figsize=(16, 8))
plt.hist(arr, bins=bins, color="blue", edgecolor="black")
plt.xticks(range(min_pos, max_pos + 1))
plt.xlabel("Final Position")
plt.ylabel("Frequency")
plt.title("Histogram of Electron Random Walk (Unit Steps)")
plt.grid(True)
plt.show()
