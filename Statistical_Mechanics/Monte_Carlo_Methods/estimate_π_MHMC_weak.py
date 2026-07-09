#Estimating Value of Pi using Metropolis Hasting Markov Chain Model
# For starters we are taking a bad target density function 1/x and this proposal is symmetric
import numpy as np
import matplotlib.pyplot as plt
import random
import plotly.graph_objects as go


def r(a,b):
    return a**2+b**2

def generate(N,epsilon):
    # Starting Point take a corner
    x=[]
    y=[]
    x.append(-1)
    y.append(-1)
    k=0
    while (k!=N):
        random_x = np.random.uniform(low=x[k]-epsilon, high=x[k]+epsilon)
        random_y = np.random.uniform(low=y[k]-epsilon, high=y[k]+epsilon)
        if(random_x<=1 and random_x>=-1 and random_y<=1 and random_y>=-1):
            alpha=r(random_x,random_y)/r(x[k],y[k])
            alpha=min(1,alpha)
            u=random.uniform(0,1)
            if(u<alpha):
                x.append(random_x)
                y.append(random_y)
            else:
                x.append(x[k])
                y.append(y[k])
            k+=1
        
    r_vals = r(np.array(x), np.array(y))

    inside = r_vals < 1

    weights = 1 / r_vals

    numerator = np.sum(weights[inside])
    denominator = np.sum(weights)

    estimate = 4 * numerator / denominator
    print(estimate)
    return x,y
    
#LOGIC OVER    

    
#------------- MATPLOTLIB VERSION-------------
def run_matplotlib(N,epsilon):
    x,y=generate(N,epsilon)
    
    burn = int(0.2 * len(x))
    x = x[burn:]
    y = y[burn:]

    step = 50000
    x = x[::step]
    y = y[::step]

    #Plot trajectory
    plt.plot(x, y, linewidth=0.8)

    plt.scatter(x[0], y[0], s=30)     # start
    plt.scatter(x[-1], y[-1], s=30)   # end

    #Draw unit circle
    theta = np.linspace(-np.pi, np.pi, 1000)
    plt.plot(np.cos(theta), np.sin(theta), linewidth=3,color='black')

    plt.axis('equal')
    plt.grid()
    plt.title("Metropolis-Hastings Trajectory")
    plt.show()
    
    
# ------------------ PLOTLY VERSION ------------------
def run_plotly(N, epsilon):
    
    a, b = generate(N, epsilon)

    #Burn-in removal
    burn = int(0.2 * len(a))
    a = np.array(a[burn:])
    b = np.array(b[burn:])

    #Downsampling
    max_points = 500
    if len(a) > max_points:
        step = int(np.ceil(len(a) / max_points))
        a = a[::step]
        b = b[::step]

    fig = go.Figure()

    #Trajectory
    fig.add_trace(go.Scatter(x=a, y=b ,mode='lines', line=dict(width=1.5,color='black'),name='Trajectory'))

    fig.add_trace(go.Scatter(x=[a[0]],y=[b[0]],mode='markers',marker=dict(size=20),name='Start'))

    fig.add_trace(go.Scatter(x=[a[-1]],y=[b[-1]],mode='markers',marker=dict(size=20, symbol='x'),name='End'))

    # ---- Unit circle ----
    theta = np.linspace(-np.pi, np.pi, 400)
    
    fig.add_trace(go.Scatter(x=np.cos(theta),y=np.sin(theta),mode='lines',line=dict(width=2,color='red'),name='Unit Circle',))

    # ---- Layout ----
    fig.update_layout(
        title="Metropolis–Hastings Trajectory",
        autosize=True,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(range=[-1,1], title="X", showgrid=False),
        yaxis=dict(range=[-1,1], title="Y", showgrid=False),
        showlegend=True
    )

    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    fig.update_layout(
    title=dict(
        text="Metropolis–Hastings Trajectory<br>"
             "<sup>Sampling inside unit disk for π estimation</sup>",
        x=0.5
    ),font=dict(size=23))
    
    fig.add_annotation(
    x=0.5,
    y=-0.19,
    xref="paper",yref="paper",
    text=("Metropolis–Hastings sampling inside the unit disk.<br> "
        "Points represent the Markov chain trajectory after burn-in.<br> "
        "Used to estimate π using 1/x for probability density which is a very weak function.<br>")
    ,align="center", font=dict(size=20),)
    
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=150))
    fig.write_html("Monte_Carlo_Methods/web_src/estimate_pi_MHMC_weak.html",config={"responsive": True})
    fig.show(config={"responsive": True})
    
run_plotly(100000,0.04)    
            

    
    
    