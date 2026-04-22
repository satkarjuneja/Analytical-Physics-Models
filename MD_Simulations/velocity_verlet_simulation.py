import numpy as np
import matplotlib.pyplot as plt

sigma=1
epsilon=1

def distance(x1,y1,z1,x2,y2,z2):
    return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**(0.5)

def leonard_jones(r):
    return 4*epsilon*(((sigma)/r)**12-((sigma)/r)**6)

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
            

def generate(N,steps,epsilon,delta_t,L,m):
    
    X = []
    Y = []
    Z = []
    
    Vx=np.random.uniform(-0,0,size=N) 
    Vy=np.random.uniform(-0,0,size=N) 
    Vz=np.random.uniform(-0,0,size=N)

    r_min = 0.1  # Settings a minimum distance between 2 atoms so that force dosent blow up

    while len(X) < N:
        x = np.random.uniform(-L, L)
        y = np.random.uniform(-L, L)
        z = np.random.uniform(-L, L)
        
        ok = True
        for i in range(len(X)):
            dx = x - X[i]
            dy = y - Y[i]
            dz = z - Z[i]
            r = np.sqrt(dx*dx + dy*dy + dz*dz)
            
            if r < r_min: # only append if molecules are far enough
                ok = False
                break
        
        if ok:
            X.append(x)
            Y.append(y)
            Z.append(z)

    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    
    X_ini=X.copy()
    Y_ini=Y.copy()
    Z_ini=Z.copy()
    
    F=np.array([force(i,X,Y,Z,N) for i in range(N)]) # Calculate Force Initial
    
    U_ini=0
    for i in range(N):
        for j in range(i+1,N):
            if(i!=j):
                U_ini+=leonard_jones(distance(X[i],Y[i],Z[i],X[j],Y[j],Z[j])) # Calculating U initial
                
    U_old=U_ini
    U_new=0
    while(True):
        
        ax=F[:,0]/m
        ay=F[:,1]/m # Accelaration
        az=F[:,2]/m
        
    
        X=X+Vx*delta_t+0.5*(ax)*(delta_t**2)  # Velocity Verlet Algorithm
        Y=Y+Vy*delta_t+0.5*(ay)*(delta_t**2)
        Z=Z+Vz*delta_t+0.5*(az)*(delta_t**2)
        
        F_new=np.array([force(i,X,Y,Z,N) for i in range(N)]) # Calculate Force
        
        ax_new=F_new[:,0]/m
        ay_new=F_new[:,1]/m
        az_new=F_new[:,2]/m
        
        Vx=Vx+(0.5)*(ax+ax_new)*delta_t
        Vy=Vy+(0.5)*(ay+ay_new)*delta_t
        Vz=Vz+(0.5)*(az+az_new)*delta_t
        
        U_new=0
        for i in range(N):
            for j in range(i+1,N):
                if(i!=j):
                    U_new+=leonard_jones(distance(X[i],Y[i],Z[i],X[j],Y[j],Z[j]))
                    
        if(abs(U_new-U_old)<epsilon):  # Stopping Condition
            break
        
        U_old=U_new
                     
    print(f"U Initial:{U_ini}")
    print(f"U Final:{U_new}")
    
    return X_ini,Y_ini,Z_ini,X,Y,Z
    
def run_matplotlib(N,steps,epsilon,delta_t,L,m):
    X_ini,Y_ini,Z_ini,X,Y,Z=generate(N,steps,epsilon,delta_t,L,m)
    
    fig = plt.figure(figsize=(10,5))

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(X_ini, Y_ini, Z_ini)
    ax1.set_title("Initial")

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(X, Y, Z)
    ax2.set_title("Final")

    plt.show()
    
run_matplotlib(108,0,0.001,0.0001,10,1)
    
    
        
    

        
        
        
    
   
        
    
    