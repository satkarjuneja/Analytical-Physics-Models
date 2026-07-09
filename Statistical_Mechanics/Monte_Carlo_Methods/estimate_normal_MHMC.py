# We are going to apply MHMC to standard normal distribution
# I am going to use 1/2exp(-mod(x)) as my q(x)
import numpy as np
import matplotlib.pyplot as plt
import random

e = np.e

def generate(N, epsilon):
    x = []
    #Start as origin
    x.append(0)

    k = 0
    while k != N:
        
        random_x = x[k] + np.random.laplace(loc=0.0, scale=epsilon) # laplacian is the exp function as defined above

        # target π(x):  exp(-x^2 / 2)
        pi_new = np.exp(-random_x**2 / 2)
        pi_old = np.exp(-x[k]**2 / 2)

        #since q is symmetric that factor cancels out
        alpha = min(1.0, pi_new / pi_old)

        u = random.uniform(0, 1)

        if u < alpha:
            x.append(random_x)
        else:
            x.append(x[k])

        k += 1

    return x


def run_matplotlib(N, epsilon):
    
    x = generate(N, epsilon)
    
    # To check accuracy
    mean=np.mean(x)
    var=np.var(x)
    #For Accuracy Calculate and compare mean and var with 0,1 respectivelty(standard gaussian has mean=0 and var=1)
    plt.hist(x, bins=60, density=True, alpha=0.5)
    
    plt.text(0.95, 0.95,
        f"Mean = {mean:.5f}\n Var={var:.5f}",
        transform=plt.gca().transAxes,
        ha='right', va='top',
        fontsize=14) 
    
    X = np.linspace(-5, 5, 1000)
    plt.plot(X, np.exp(-X**2 / 2) / np.sqrt(2*np.pi))

    plt.show()


run_matplotlib(1000000, 0.2)