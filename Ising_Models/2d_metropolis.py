import numpy as np
import matplotlib.pyplot as plt

# red is upspin blue is downspin
k=1 # Boltzmann constant in arbitrary units (SI UNIT 10^-23 was causing overflow issues)

def pdf(T,change):
    return np.exp((-1)*change/(k*T))

def accept(grid,point,N,T,J,x,y):
    
    spin=grid[x][y]
    new=(-1)*grid[x][y]
    
    INITIAL=J*spin*(grid[(x-1)%N][y]+grid[(x+1)%N][y]+grid[x][(y-1)%N]+grid[x][(y+1)%N])
    
    FINAL=J*new*(grid[(x-1)%N][y]+grid[(x+1)%N][y]+grid[x][(y-1)%N]+grid[x][(y+1)%N])
    
    change=FINAL-INITIAL
    
    if(change<0):
        return True,change
    else:
        x=np.random.uniform()
        if(x<pdf(T,change)):
            return True,change
        else:
            return False,change
            

def total_energy(grid, N, J):
    e = 0
    for i in range(N):
        for j in range(N):
            spin = grid[i][j]
            e += J * spin * (grid[(i-1) % N][j] +grid[(i+1) % N][j] +grid[i][(j-1) % N] +grid[i][(j+1) % N])
    return e
    
# make an N*N grid 
def generate(N,epsilon,steps,J,T):
        
    initial_random_values=np.random.choice([-1, 1], size=N*N)
    
    grid=initial_random_values.reshape(N,N)
    ini_grid=grid.copy()
    #Now the Algorithm
    old_E=total_energy(grid,N,J)
    
    LIMIT=steps*N*N  # Cause one monte carlo step is one step
    for i in range(LIMIT):
        
        point=np.random.randint(0,N*N) # random point to flip
        
        # Assuming J to be isotropic and external magnetic field to be zero
        
        y=int(point%N)
        x=int(point/N)
        acc=accept(grid,point,N,T,J,x,y)
        
        if(acc[0]): # if accepted flip the spin
            grid[x][y]=(-1)*grid[x][y]
            new_E=old_E+acc[1] # change
            if(abs(new_E-old_E)<epsilon):
                break
            old_E=new_E
        
        
        
    return grid,ini_grid
    
def run_matplotlib(N,epsilon,steps,J,T):
    grid,ini_grid=generate(N,epsilon,steps,J,T)
    
    x, y = np.meshgrid(np.arange(N), np.arange(N))

    fig, axes = plt.subplots(2, 2,figsize=(8,8))  # 2 rows, 2 columns

    axes = axes.flatten()

    axes[0].scatter(x.flatten(), y.flatten(),
                    c=ini_grid.flatten(), cmap='bwr')
    axes[0].set_aspect('equal')
    axes[0].grid(True)
    axes[0].set_title("Initial")

    axes[1].scatter(x.flatten(), y.flatten(),
                    c=grid.flatten(), cmap='bwr')
    axes[1].set_aspect('equal')
    axes[1].grid(True)
    axes[1].set_title("Step 1")

    axes[2].imshow(ini_grid, cmap='bwr',
                interpolation='bicubic',
                origin='lower')
    axes[2].set_title("Step 2")

    axes[3].imshow(grid, cmap='bwr',
                interpolation='bicubic',
                origin='lower')
    axes[3].set_title("Final")

    plt.show()
    
    
N=int(input("Enter Number of electrons in a row: "))
T=float(input("Enter Temperature: "))
run_matplotlib(N,0.0001,100000,1,T)
    
    