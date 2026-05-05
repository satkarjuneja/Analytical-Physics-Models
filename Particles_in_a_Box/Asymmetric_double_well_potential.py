import numpy as np
import matplotlib.pyplot as plt
import random

def U(x,y):
    return (x**2-1)**2+(y**2-1)**2+(x**2)*y/2
def Fx(x,y):
    return -(2*(x**2-1)*(2*x)+x*y)
def Fy(x,y):
    return -(2*(y**2-1)*(2*y)+x**2/2)

xchar=input("Enter The Initial X-Coordinate: ")
ychar=input("Enter The Initial Y-Coordinate: ")
x0=float(xchar)
y0=float(ychar)
xdata=[]
ydata=[]
ep=0.0008
alp=0.01
x=x0
y=y0
Udata=[]
step=[]

plt.ion()
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(121)  
ax2 = fig.add_subplot(122, projection='3d') 

xv = np.linspace(-3, 3, 200)
yv = np.linspace(-3, 3, 200)
X, Y = np.meshgrid(xv, yv)
Z = U(X, Y)
surf = ax2.plot_surface(X, Y, Z, cmap='inferno', linewidth=0, antialiased=True)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_zlabel('U(x,y)')
ax2.set_title('3D Potential Surface')

for i in range(1000):
    step.append(i)
    x += alp * Fx(x,y)
    y += alp * Fy(x,y)
    xdata.append(x)
    ydata.append(y)
    Udata.append(U(x,y))

    ax1.cla()
    ax1.grid(True)
    ax1.plot(step, Udata, color='black', linestyle='-')
    ax1.set_xlabel('Step')
    ax1.set_ylabel('U(x,y)')
    ax1.set_title('Potential vs Step')

    plt.pause(0.001)
    ax1.text(0.5, 0.5, f"x={x:.4f}, y={y:.4f}, U={U(x,y):.4f}",
        ha='center', va='center', fontsize=10, transform=ax1.transAxes)

    if (Fx(x,y)<ep and Fx(x,y)>-ep and Fy(x,y)<ep and Fy(x,y)>-ep):
        plt.pause(2)
        break

    print(x, y, U(x,y))

plt.ioff()
plt.show()
