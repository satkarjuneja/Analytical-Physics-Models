import numpy as np
import matplotlib.pyplot as plt

def euler(t,w):
    return np.exp(-1j * w * t)

def gauss(t):
    return np.exp(-t**2)

def gauss(t):
    return np.exp(-t**2)

def X_k(N, k, T):
    t = np.linspace(-5, 5, N)         # time samples
    w = 2 * np.pi * k / T
    X = gauss(t) * euler(t,w)
    return np.sum(X) * (t[1]-t[0])      # scale by Δt

def generate(N, K, T):
    k = np.linspace(-5, 5, K)
    F = np.array([X_k(N, ki, T) for ki in k])  # compute each frequency
    plt.plot(k, np.abs(F))
    plt.plot(k,np.exp(-k**2))
    plt.title("Amplitude spectrum")
    plt.xlabel("Frequency/Time")
    plt.ylabel("|F(w)|")
    plt.grid()
    plt.show()

generate(1000, 1000, 2)