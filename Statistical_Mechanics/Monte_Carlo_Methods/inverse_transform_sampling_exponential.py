# We are going to perform Inverse Transform Sampling of lambda*e^(-lambda*x) this is the PDF(probabiliy distribution function)
#First: we will calculate the CDF
#Then use uniform random generation  and compute inverse CDF

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

e=np.e

def generate(N,lambd):
    U=np.random.uniform(0,1,size=N)
    inverse_CDF=(-1/lambd)*np.log(1-U)
    return inverse_CDF

def run_matplotlib(N,lambd):
    X=generate(N,lambd)
    plt.hist(X, bins=40, density=True, color='blue')

    x = np.linspace(0, np.max(X), 1000)
    plt.plot(x, lambd * np.exp(-lambd * x), color='black')
    plt.grid()
    plt.show()

def run_plotly(N, lambd):
    X = generate(N, lambd)

    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=X,
        nbinsx=60,
        histnorm='probability density',
        name='Samples'
    ))

    # PDF curve
    x = np.linspace(0, np.max(X), 1000)
    pdf = lambd * np.exp(-lambd * x)

    fig.add_trace(go.Scatter(
        x=x,
        y=pdf,
        mode='lines',
        name='PDF'
    ))

    fig.update_layout(
        title="Exponential Distribution via Inverse Transform Sampling",
        xaxis_title="x",
        yaxis_title="Density"
    )
    
    fig.update_layout(
    title=dict(
        text="Inverse Transform Sampling<br>"
             "<sup>Sampling Exponential Function </sup>",
        x=0.5
    ),font=dict(size=23))
    
    fig.update_layout(margin=dict(l=0, r=0, t=70, b=0))
    fig.write_html("Monte_Carlo_Methods/web_src/inverse_transform_sampling_exponential.html",config={"responsive": True})
    fig.show(config={"responsive": True})

    fig.show()
    
    
# run_matplotlib(100000,100)
run_plotly(100000,100)

