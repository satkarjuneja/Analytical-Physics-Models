# We are going to apply MHMC to N(0,1)+N(1,2)+N(2,3)
# I am going to use exp(-mod(x)) as my q(x)
import numpy as np
import matplotlib.pyplot as plt
import random

e = np.e

def scale(sigma):
    return 1/(2*np.pi*sigma**2)**0.5

def pi(x):
    return np.exp(-x**2 / 2)*scale(1)+np.exp(-(x-1)**2/8)*scale(2)+np.exp(-(x-2)**2/18)*scale(3)
    

def generate(N, epsilon):
    x = []
    #Start as origin
    x.append(0)

    k = 0
    while k != N:
        
        random_x = x[k] + np.random.laplace(loc=0.0, scale=epsilon)

        # target π(x): exp(-x^2 / 2)
        pi_new = pi(random_x)
        pi_old = pi(x[k])

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
    #For Accuracy Calculate and compare mean and var with 0,16/3 respectivelty(calculated)
    plt.hist(x, bins=60, density=True, alpha=0.5)
    
    plt.text(0.95, 0.95,
        f"Mean = {mean:.5f}\n Var={var:.5f}",
        transform=plt.gca().transAxes,
        ha='right', va='top',
        fontsize=14) 
    
    X = np.linspace(-5, 5, 1000)
    plt.plot(X, pi(X)/ np.sqrt(2*np.pi))

    plt.show()


run_matplotlib(1000000, 0.2)