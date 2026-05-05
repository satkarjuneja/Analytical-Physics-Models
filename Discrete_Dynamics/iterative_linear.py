import numpy as np 
import matplotlib.pyplot as plt

def iterative_map(x,m):
    return x*m

def generate(N,m,x0):
    Y=[]
    Y.append(x0)
    prev=x0
    for i in range(N):
        x=iterative_map(prev,m)
        Y.append(x)
        prev=x
    return Y

def run_matplotlib(N,m,x0):
    Y = generate(N,m,x0)
    iterations = np.arange(len(Y))
    plt.plot(iterations, Y, marker='o', markersize=2)
    plt.xlabel("Iteration n")
    plt.ylabel("x_n")
    plt.title(f"Linear map: x_n+1 = {m}*x_n")
    plt.grid()
    plt.show()
    
run_matplotlib(100,-0.9,1)