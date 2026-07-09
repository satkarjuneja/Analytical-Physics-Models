import numpy as np
import matplotlib.pyplot as plt

# Unifrom Standard Monte Carlo

N = 20000000

random_x = np.random.uniform(0, 10, N)
random_y = np.random.uniform(0, 1, N)

is_below = (np.exp(-random_x**2) > random_y)
num_below = np.sum(is_below)

estimate_uniform = 20 * num_below / N

# Importance sampling (Gaussian)
#We are choosing Gaussian as our importance function

x_gauss = np.random.normal(0, 1, N)
weights = np.sqrt(2*np.pi) * np.exp(-x_gauss**2 / 2)
estimate_importance = np.mean(weights)


fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Left plot Orignal
x = np.linspace(0, 10, 1000)
ax[0].scatter(random_x[:5000], random_y[:5000], s=1)
ax[0].plot(x, np.exp(-x**2), color='black')
ax[0].grid()
ax[0].text(
    0.95, 0.99,
    f"Uniform = {estimate_uniform:.6f}",
    transform=ax[0].transAxes,
    ha='right',
    va='top'
)

# Right plot Gaussian
ax[1].hist(x_gauss, bins=100, density=True)
x2 = np.linspace(-5, 5, 1000)
ax[1].plot(x2, (1/np.sqrt(2*np.pi))*np.exp(-x2**2/2), color='black')
ax[1].grid()
ax[1].text(
    0.95, 0.99,
    f"Importance = {estimate_importance:.6f}",
    transform=ax[1].transAxes,
    ha='right',
    va='top'
)

plt.show()