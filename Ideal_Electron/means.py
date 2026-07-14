import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def generate_walk(steps, electrons):
    positions = np.zeros(electrons)
    mean = []
    meansq = []
    x_sample = []

    for i in range(steps):
        num = np.random.choice([1, -1], size=electrons)
        positions += num

        mean.append(np.mean(positions))
        meansq.append(np.mean(positions**2))
        x_sample.append(positions[0])

    return mean, meansq, x_sample


def run_plotly(steps=50000, electrons=10000):
    mean, meansq, x_sample = generate_walk(steps, electrons)

    fig = make_subplots(
        rows=1, cols=3, subplot_titles=("Sample Electron Walk", "Mean ⟨x⟩", "Mean ⟨x²⟩")
    )

    # x-axis (step index)
    steps_axis = list(range(len(x_sample)))

    # 1st plot
    fig.add_trace(go.Scatter(x=steps_axis, y=x_sample, mode="lines"), row=1, col=1)

    # 2nd plot
    fig.add_trace(
        go.Scatter(x=steps_axis, y=mean, mode="lines", name="⟨x⟩"), row=1, col=2
    )

    # 3rd plot
    fig.add_trace(
        go.Scatter(
            x=steps_axis, y=meansq, mode="lines", name="⟨x²⟩", line=dict(color="red")
        ),
        row=1,
        col=3,
    )

    fig.update_xaxes(title_text="Step", row=1, col=1)
    fig.update_xaxes(title_text="Step", row=1, col=2)
    fig.update_xaxes(title_text="Step", row=1, col=3)

    fig.update_yaxes(title_text="Position", row=1, col=1)
    fig.update_yaxes(title_text="⟨x⟩", row=1, col=2)
    fig.update_yaxes(title_text="⟨x²⟩", row=1, col=3)

    fig.update_layout(title="Electron Random Walk Statistics")

    fig.write_html("Ideal_Electron/web_src/means.html")
    fig.show()


# if __name__ == "__main__":
run_plotly()
