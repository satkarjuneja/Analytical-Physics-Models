# Why 108 particles ?<br>
**Berni Alder and Thomas Wainwright** at Lawrence Livermore National Laboratory, in their 1957 paper *"Phase Transition for a Hard Sphere System"* published in the *Journal of Chemical Physics*. The 108-particle number wasn't arbitrary it corresponds to a 3×3×3
3×3×3 replication of a unit cell with 4 particles (FCC arrangement),<br> giving 4×27= 108<br>
which allowed periodic boundary conditions to work cleanly with an FCC lattice.
This simulation used hard-sphere potentials (perfectly elastic collisions, no continuous force field), so it was event-driven rather than the force-integration style you'd recognize from modern MD. The continuous-potential, Verlet-integrator style came later with Rahman's 1964 liquid argon simulation.
This was the first MD simulation