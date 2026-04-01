import numpy as np
import matplotlib.pyplot as plt

r_values = np.linspace(2.5, 4.0, 1200)
x0 = 0.5
N = 1000
transient = 500

for r in r_values:
    x = x0
    xs = []
    for i in range(N):
        x = r*x*(1-x)
        if i >= transient:
            xs.append(x)
    plt.plot([r]*len(xs), xs, ',k')

plt.xlabel("r")
plt.ylabel("x")
plt.title("Logistic Map Bifurcation Diagram")
plt.show()