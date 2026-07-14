import numpy as np
import matplotlib.pyplot as plt

walks = 100000
num_steps = 10000

final_positions = []

for _ in range(walks):
    steps = np.random.choice([-1, 1], size=num_steps)
    position = np.sum(steps)
    final_positions.append(position)

final_positions = np.array(final_positions)
min_pos = final_positions.min()
max_pos = final_positions.max()
bins = np.arange(min_pos - 0.5, max_pos + 0.5, 1)

plt.figure(figsize=(16, 8))
plt.hist(final_positions, bins=bins, color="blue", edgecolor="black")
plt.xticks(range(min_pos, max_pos + 1))
plt.xlabel("Final Position")
plt.ylabel("Frequency")
plt.title("Histogram of Electron Random Walk (Unit Steps)")
plt.grid(True)
plt.show()
