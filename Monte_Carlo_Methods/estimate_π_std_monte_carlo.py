import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import random

# Calculate value of Pi using ratio of a area of a square and a circle

N=10000000 # Number of Random Numbers
random_x = np.random.uniform(low=0, high=1, size=N)
random_y = np.random.uniform(low=0, high=1, size=N)

is_inside= ((random_x)**2+(random_y)**2<1)
# changed the sum to cumsum to obtain value for each i
number_inside=np.cumsum(is_inside)
indices = np.arange(1, N + 1)
estimate = 4* (number_inside)/(indices)

#Making the circle
theta=np.linspace(0,np.pi/2,10000)
circle_x=np.cos(theta)
circle_y=np.sin(theta)

pi_est = 4 * number_inside[-1] / N

fig, axs = plt.subplots(1, 2, figsize=(14, 6))  # 1 row, 2 columns

#First plot (scatter + circle)
axs[0].scatter(random_x[:5000], random_y[:5000], s=1)
axs[0].plot(circle_x, circle_y, color='black')
axs[0].set_aspect('equal')
axs[0].grid()
axs[0].set_title(f"$\\pi \\approx {pi_est:.6f}$")

#Second plot (convergence)
factor = 1000
axs[1].semilogx(indices[::factor], estimate[::factor], label='Monte Carlo Estimate')
axs[1].axhline(y=np.pi, linestyle='--', label='True $\\pi$')
axs[1].set_title(f"Convergence of $\\pi$ Estimate over $N={N}$ Samples")
axs[1].set_xlabel("Number of Samples ($N$) - Log Scale")
axs[1].set_ylabel("Estimated Value")
axs[1].grid(True, which="both", linestyle='--', alpha=0.5)
axs[1].set_ylim(3.10, 3.20)
axs[1].legend()

plt.tight_layout()
plt.show()
