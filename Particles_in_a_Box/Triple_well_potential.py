import numpy as np
import matplotlib.pyplot as plt
import random

xchar=input("Initial Value of X: ")
x0=float(xchar)
x=x0
Udata=[]
xprev=0
def U(x):
    return x**6-5*x**4+4*x**2
def derivative(x):
    return 6*x**5-20*x**3+8*x
# Umin1=0
# Umin2=-6.06
alpha=0.009
ep=0.001
plt.ion()
fig, ax = plt.subplots()
for i in range(1000):
    F = -derivative(x)
    xprev = x
    x = x + alpha * F
    print(x, U(x))
    Udata.append(U(x))
    plt.cla()
    plt.grid(True)
    # print(Udata)
    plt.plot(range(len(Udata)), Udata, color='black', linestyle='-')
    plt.pause(0.1)
    print(F)
    if (F<ep and F > -ep):
        break

plt.ioff()
plt.show()
