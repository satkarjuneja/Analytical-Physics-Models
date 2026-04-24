import numpy as np
import matplotlib.pyplot as plt

sigma = 1
epsilon = 1

def distance(x1,y1,z1,x2,y2,z2):
    return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5

def leonard_jones(r):
    return 4*epsilon*((sigma/r)**12 - (sigma/r)**6)

def force(i, X, Y, Z, N):
    Fx, Fy, Fz = 0.0, 0.0, 0.0
    
    for j in range(N):
        if j == i:
            continue
        
        x = X[i] - X[j]
        y = Y[i] - Y[j]
        z = Z[i] - Z[j]
        
        r = np.sqrt(x*x + y*y + z*z)
        if r == 0:
            continue
        
        f = 24*epsilon*(2*(sigma**12)/(r**13) - (sigma**6)/(r**7))
        
        Fx += f * x / r
        Fy += f * y / r
        Fz += f * z / r
    
    return np.array([Fx, Fy, Fz])


def generate(N, steps,delta_t, L, m):
    rng = np.random.default_rng(38)
    
    avg_V = []
    avg_E = []
    sample_pos = []
    time = []
    
    X, Y, Z = [], [], []
    
    Vx = rng.uniform(-1,1,size=N)
    Vy = rng.uniform(-1,1,size=N)
    Vz = rng.uniform(-1,1,size=N)

    r_min = 0.1
    
    while len(X) < N:
        x = rng.uniform(-L, L)
        y = rng.uniform(-L, L)
        z = rng.uniform(-L, L)
        
        ok = True
        for i in range(len(X)):
            dx = x - X[i]
            dy = y - Y[i]
            dz = z - Z[i]
            r = np.sqrt(dx*dx + dy*dy + dz*dz)
            
            if r < r_min:
                ok = False
                break
        
        if ok:
            X.append(x)
            Y.append(y)
            Z.append(z)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    
    X_ini = X.copy()
    Y_ini = Y.copy()
    Z_ini = Z.copy()
    
    F = np.array([force(i,X,Y,Z,N) for i in range(N)])
    
    # initial potential energy
    U = 0
    for i in range(N):
        for j in range(i+1, N):
            U += leonard_jones(distance(X[i],Y[i],Z[i],X[j],Y[j],Z[j]))

    for ti in range(steps*N*N): # Monte Carlo Steps
        
        ax = F[:,0]/m
        ay = F[:,1]/m
        az = F[:,2]/m
        
        # position
        X = X + Vx*delta_t + 0.5*ax*(delta_t**2)
        Y = Y + Vy*delta_t + 0.5*ay*(delta_t**2)
        Z = Z + Vz*delta_t + 0.5*az*(delta_t**2)
        
        # recalculate forces
        F_new = np.array([force(i,X,Y,Z,N) for i in range(N)])
        
        ax_new = F_new[:,0]/m
        ay_new = F_new[:,1]/m
        az_new = F_new[:,2]/m
        
        # velocity update
        Vx = Vx + 0.5*(ax + ax_new)*delta_t
        Vy = Vy + 0.5*(ay + ay_new)*delta_t
        Vz = Vz + 0.5*(az + az_new)*delta_t
        
        F = F_new
        
        U = 0
        for i in range(N):
            for j in range(i+1, N):
                U += leonard_jones(distance(X[i],Y[i],Z[i],X[j],Y[j],Z[j]))
        
        K = 0.5 * m * np.sum(Vx**2 + Vy**2 + Vz**2)
        
        avg_E.append(K + U)
        
        v_mag = np.sqrt(Vx**2 + Vy**2 + Vz**2)
        avg_V.append(np.mean(v_mag))
        
        sample_pos.append(np.sqrt(X[0]**2 + Y[0]**2 + Z[0]**2))
        
        time.append(ti)
        print(f"Step: {ti}",end='\r')

    print(f"Initial Energy: {avg_E[0]}")
    print(f"Final Energy: {avg_E[-1]}")
    
    return X_ini,Y_ini,Z_ini,X,Y,Z,sample_pos,avg_E,avg_V,time


def run_matplotlib(N,steps,delta_t,L,m):
    X_ini,Y_ini,Z_ini,X,Y,Z,avg_pos,avg_E,avg_V,time = generate(N,steps,delta_t,L,m)
    
    fig = plt.figure(figsize=(12,8))

    ax1 = fig.add_subplot(231, projection='3d')
    ax1.scatter(X_ini, Y_ini, Z_ini)
    ax1.set_title("Initial")

    ax2 = fig.add_subplot(232, projection='3d')
    ax2.scatter(X, Y, Z)
    ax2.set_title("Final")

    ax3 = fig.add_subplot(233)
    ax3.plot(time[2000:], avg_pos[2000:])
    ax3.grid()
    ax3.set_title("Sample Position vs Time")

    ax4 = fig.add_subplot(234)
    ax4.plot(time[2000:], avg_V[2000:])
    ax4.grid()
    ax4.set_title("Avg Velocity vs Time")

    ax5 = fig.add_subplot(235)
    ax5.plot(time[2000:], avg_E[2000:])
    ax5.grid()
    ax5.set_title("Total Energy vs Time")

    plt.tight_layout()
    plt.show()

# n,steps,time,L,m
run_matplotlib(10, 300,0.0001, 3, 1)