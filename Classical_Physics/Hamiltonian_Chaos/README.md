# Hénon-Heiles System — Hamiltonian Chaos

> This is my first Julia simulation :)

## The System

The Hénon-Heiles system is a 2D Hamiltonian originally studied by Michel Hénon and Carl Heiles in 1964 to investigate whether stellar orbits in a galaxy possess a third integral of motion beyond energy and angular momentum.

The Hamiltonian is a 2D harmonic oscillator perturbed by a cubic term:

$$H = \frac{1}{2}(p_x^2 + p_y^2) + \frac{1}{2}(x^2 + y^2) + x^2 y - \frac{y^3}{3}$$


## Poincaré Sections

Since the full phase space is 4D (x, y, px, py), direct visualization is impossible. A Poincaré section reduces this to 2D by recording the system state only when the trajectory crosses the plane y = 0 with py > 0 once per orbit. The resulting plot of (x, px) reveals the structure of phase space:

- **Ordered regime (E = 0.08):** Points from each trajectory trace smooth closed curves cross-sections of [KAM](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Arnold%E2%80%93Moser_theorem)
 tori.

- **Mixed regime (E = 0.12):** Some tori survive, others break. Islands of stability coexist with a thin chaotic sea

- **Chaotic regime (E = 0.167):** Near the escape energy, most tori have dissolved. Points scatter across the entire allowed region. No third integral exists here.

## Integrator

The simulation uses the **Störmer-Verlet symplectic integrator**:

1. Half-kick momenta using current forces
2. Full-drift positions using half-step momenta
3. Half-kick momenta again using updated forces

The key property is symplecticity — the integrator exactly preserves the geometric structure of Hamiltonian mechanics, meaning energy is conserved to machine precision over millions of steps. A naive Euler integrator would show visible energy drift, corrupting the Poincaré sections entirely.


## References

- Hénon & Heiles, *The Applicability of the Third Integral of Motion*, The Astronomical Journal, 1964
- Landau & Lifshitz, *Classical Mechanics*, §49–50 (action-angle variables, integrable systems)
