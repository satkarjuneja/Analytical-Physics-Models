# We have to estimate the value of Expectation(X**2) where X is sampled from exp(-x^4)/Z
# where Z is just some normalization constant
# lets choose simple e^(-x**2)/sqrt(pi)
import numpy as np
import matplotlib.pyplot as plt

e = np.e

Z = (np.pi) ** 0.5


def generate(N):
    x = np.random.normal(
        0, (1 / 2) ** 0.5, size=N
    )  # Sampling from normal distribution as our sampling distribution

    EX2_without_norm = (x**2) * (e ** (-(x**4) + x**2))
    norm = e ** (-(x**4) + x**2)
    EX2_cumu = np.cumsum(EX2_without_norm)
    norm_cumu = np.cumsum(norm)
    EX2 = EX2_cumu / norm_cumu
    return EX2, x


def run_matplotlib(N):
    True_value = 0.3379891200  # using calculator to judge accuracy
    EX2, x = generate(N)
    plt.plot(EX2)

    final_est = EX2[-1]

    plt.text(
        0.95,
        0.95,
        f"Estimate ≈ {final_est:.8f}",
        transform=plt.gca().transAxes,
        ha="right",
        va="top",
        fontsize=14,
    )

    plt.text(
        0.95,
        0.8,
        f"True_Value ≈ {True_value}",
        transform=plt.gca().transAxes,
        ha="right",
        va="top",
        fontsize=14,
    )

    plt.axhline(True_value, color="black")
    plt.xlabel("Number of samples")
    plt.ylabel("Estimate of E[X^2]")
    plt.grid()
    plt.show()
    print(EX2)


run_matplotlib(100000)
