import numpy as np
import matplotlib.pyplot as plt
import random
import plotly.graph_objects as go


def generate_walk(Num=1000):
    position = 0
    step_data = [0]
    location_data = [0]

    for i in range(1, Num + 1):
        step = random.choice([1, -1])
        position += step
        step_data.append(i)
        location_data.append(position)

    return step_data, location_data


# ------------------ MATPLOTLIB VERSION ------------------
def run_matplotlib():
    step_data = [0]
    location_data = [0]
    position = 0

    plt.ion()
    fig, ax = plt.subplots()
    plt.title("Drunkard (Matplotlib)")
    plt.xlabel("Steps")
    plt.ylabel("Location")
    plt.grid(True)

    for i in range(1, 1000):
        step = random.choice([1, -1])
        position += step
        step_data.append(i)
        location_data.append(position)

        plt.cla()
        plt.plot(step_data, location_data, color="black", linestyle="-")
        plt.plot(i, position, "o", color="red")
        plt.grid(True)
        plt.pause(0.01)

    plt.ioff()
    plt.show()


# ------------------ PLOTLY VERSION ------------------
def run_plotly():
    step_data, location_data = generate_walk(1000)

    fig = go.Figure()

    # full path
    fig.add_trace(go.Scatter(x=step_data, y=location_data, mode="lines", name="Walk"))

    # final position
    fig.add_trace(
        go.Scatter(
            x=[step_data[-1]],
            y=[location_data[-1]],
            mode="markers",
            name="Final Position",
        )
    )

    fig.update_layout(
        title="1D Random Walk of a Drunkard",
        xaxis_title="Steps",
        yaxis_title="Location",
    )

    fig.write_html("Ideal_Electron/web_src/Walkplot.html")
    fig.show()


# run_matplotlib()
run_plotly()
