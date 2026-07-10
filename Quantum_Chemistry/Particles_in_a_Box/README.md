# 3D Particle-in-a-Box Simulations

This folder contains Python scripts for simulating **particles moving inside a 3D box**. The goal is to explore how particles distribute themselves under different potential functions and to study their position profiles.

---

## Overview

The scripts allow you to:

- Simulate the motion of particles confined in a **3D box**  
- Apply different **Potential Functions** to influence particle positions  
- Compute **Position Distributions** and observe how particles settle over time  
- Visualize the 3D trajectories and overall spatial patterns

These simulations provide a simple way to **Study particle behavior and density profiles** in a confined space using computational methods.

---

## Leonard-Jones Potential Simulation
- `Stable.py` initially generates a random configuration, then the particles are made to move along their direction of force until they achieve the most stable configuration.

- The Lennard-Jones potential is given by  
    $U(r) = 4\epsilon \left[ \left( \frac{\sigma}{r} \right)^{12} - \left( \frac{\sigma}{r} \right)^6 \right]$  
    where the symbols hold their usual meaning.

- **Method used to find minimum configuration:**  
  We calculate the force on each particle $F_x$, $F_y$, and $F_z$ By
$F_x=\frac{\partial U}{\partial x}$ <br>
$F_x = \frac{\partial U}{\partial r_{ij}} \cdot \frac{\partial r_{ij}}{\partial x}$ <br>



