# REVIEW REPORT — Analytical-Physics-Models

## 1) Short summary (top 5 issues)
1. **Critical:** `Statistical_Mechanics/Ising_Models/2d_metropolis.py` has reversed Metropolis acceptance logic/sign convention, so energetically unfavorable moves are accepted too often (breaks detailed balance).
2. **Critical:** `Quantum_Chemistry/Particles_in_a_Box/Stability_Calculation/3_stable.py` calls `dis(...)` with wrong arguments (`z_data, [j]`), which can crash at runtime and prevents stable-configuration computation.
3. **Major:** `models.json` and `backend.py` are not present in the repository, so frontend reachability and backend security checks requested in this review cannot be completed.
4. **Major:** Multiple scripts save outputs into non-existent `web_src` directories, causing runtime file-write failures.
5. **Major:** Repository lacks reproducibility/testing foundations (no Python requirements file, no Julia `Project.toml`/`Manifest.toml`, no test suite, no CI for tests).

---

## 2) Findings table

| ID | Severity | File | One-line description |
|---|---|---|---|
| F01 | Critical | `Statistical_Mechanics/Ising_Models/2d_metropolis.py` | Metropolis acceptance uses reversed energy/sign logic (violates detailed balance). |
| F02 | Critical | `Quantum_Chemistry/Particles_in_a_Box/Stability_Calculation/3_stable.py` | Wrong `dis(...)` arguments (`z_data, [j]`) break runtime and force/energy calculation. |
| F03 | Major | `Quantum_Chemistry/Particles_in_a_Box/Stability_Calculation/1_config.py` | “Force” is computed as derivative of distance, not derivative of LJ potential. |
| F04 | Major | `.gitignore` + repo root | `models.json` and `backend.py` are missing; frontend registration/security review cannot be verified. |
| F05 | Major | `.gitignore` | Critical infra files are ignored (`models.json`, `backend.py`, `Dockerfile`, `requirement.txt`). |
| F06 | Major | `README.md` | Main model links point to non-existent top-level paths. |
| F07 | Major | `Learn_Julia/3_boids_algorithm.jl` | Cohesion steering angle points away from center while comment says “towards center”. |
| F08 | Major | `Quantum_Computing/QUBO/Set_Packing.jl` | Uses `Q` before defining it; QUBO build function not invoked. |
| F09 | Major | `Ideal_Electron/Walkplot.py`, `Ideal_Electron/means.py`, `Statistical_Mechanics/Monte_Carlo_Methods/*` | HTML export paths target missing `web_src` dirs. |
| F10 | Major | `Statistical_Mechanics/Ising_Models/2d_metropolis.py` | `new_E` can be printed before assignment if no move is accepted. |
| F11 | Major | Multiple simulation dirs | Missing README files for many simulation folders. |
| F12 | Major | Repo root / Python & Julia codebase | No dependency lock/pin files (`requirements.txt`, `pyproject.toml`, Julia env files). |
| F13 | Major | `.github/workflows/static.yml` + repo root | No test suite and no CI test workflow (only GitHub Pages deploy workflow). |
| F14 | Major | `Quantum_Chemistry/Particles_in_a_Box/` | Known-suspect `box.py` is absent, so overwrite-vs-accumulate force bug cannot be verified. |
| F15 | Minor | `Statistical_Mechanics/Ising_Models/2d_metropolis.py` | Early-stop criterion uses tiny energy delta, not equilibration diagnostics. |
| F16 | Minor | Multiple scripts | Scripts run immediately on import (no `if __name__ == "__main__":`). |
| F17 | Minor | Multiple simulation scripts | No controlled random seeding for reproducibility. |
| F18 | Minor | Multiple simulation scripts/READMEs | Units are often implicit or mixed; reduced vs SI not consistently stated. |
| F19 | Minor | Repo metadata | No `CITATION` file for scientific citation/reuse. |
| F20 | Minor | Taxonomy/layout | `Ideal_Electron` is outside `Statistical_Mechanics` despite declared taxonomy. |

---

## 3) Detailed findings by part

## Part 1 — Topic coverage

### Current simulations/topics found in repo
- **Classical Physics**
  - `Classical_Physics/MD_Simulations/velocity_verlet_simulation.py`
  - `Classical_Physics/Electrodynamics/equipotential_surfaces_for_2_particles.py`
  - `Classical_Physics/Hamiltonian_Chaos/Hénon_Heiles_Model.jl`
  - `Classical_Physics/Discrete_Dynamics/logistic_map.py`
  - `Classical_Physics/Discrete_Dynamics/iterative_linear.py`
- **Statistical Mechanics**
  - `Statistical_Mechanics/Ising_Models/2d_metropolis.py`
  - `Statistical_Mechanics/Monte_Carlo_Methods/*.py` (MHMC, importance sampling, inverse transform, π estimation)
  - `Ideal_Electron/*.py` (random-walk-based electron toy models)
- **Quantum Computing & Optimization**
  - `Quantum_Computing/QUBO/Max_Cut.jl`
  - `Quantum_Computing/QUBO/Set_Packing.jl`
- **Tools & Tutorials**
  - `Learn_Julia/*.jl` + `Learn_Julia/4_differentialequations.jl/*.jl`
  - `Machine_Learning/Language_Models/*.jl`
  - `Machine_Learning/Reinforcement Learning/1_tic_tac_toe.jl`
- **Additional topics present (outside requested taxonomy)**
  - `Computational_Methods/Fourier_Analysis/*`
  - `Quantum_Chemistry/Particles_in_a_Box/*`
  - `Quantum_Chemistry/Modelling_Using_VMD/*`
  - `Quantum_Chemistry/Calculating_Activation_and_Reaction_Energy_Of_Reactions/*`

### Registration in `models.json` and frontend reachability

#### F04 (Major)
- **File/line:** `.gitignore:7,10` and repo root (missing files)
- **What is wrong:** `models.json` and `backend.py` are not present in tracked files.
- **Why it matters:** This blocks the requested verification of model registration and frontend/backend reachability/security.
- **Suggested fix:** Track `models.json` and `backend.py` in git (or provide checked-in template/test fixtures) so CI and reviewers can validate routing and execution.
- **Snippet:**
```gitignore
models.json
backend.py
```

#### F05 (Major)
- **File/line:** `.gitignore:7-10`
- **What is wrong:** Core runtime/infra files are globally ignored (`models.json`, `backend.py`, `Dockerfile`, `requirement.txt`).
- **Why it matters:** Important app behavior can drift locally and remain unreviewed/unversioned.
- **Suggested fix:** Stop ignoring source-of-truth app files; only ignore local overrides/secrets.
- **Snippet:**
```gitignore
models.json
requirement.txt
Dockerfile
backend.py
```

### Taxonomy checks

#### F20 (Minor)
- **File/line:** Repo layout (`Ideal_Electron/` at top level)
- **What is wrong:** Declared taxonomy places Ideal Electron under Statistical Mechanics, but folder is top-level.
- **Why it matters:** Navigation and frontend grouping can become inconsistent.
- **Suggested fix:** Move under `Statistical_Mechanics/Ideal_Electron` or update taxonomy/docs consistently.

### README coverage checks

#### F11 (Major)
- **File/line:** Missing README in:
  - `Classical_Physics/Discrete_Dynamics/`
  - `Classical_Physics/Electrodynamics/`
  - `Classical_Physics/MD_Simulations/`
  - `Statistical_Mechanics/Ising_Models/`
  - `Statistical_Mechanics/Monte_Carlo_Methods/`
  - `Machine_Learning/Language_Models/`
  - `Machine_Learning/Reinforcement Learning/`
  - `Quantum_Chemistry/Calculating_Activation_and_Reaction_Energy_Of_Reactions/`
- **What is wrong:** Many simulation folders have no local README.
- **Why it matters:** Missing equations/parameters/run instructions makes learning and reuse difficult.
- **Suggested fix:** Add per-folder README with physics model, equations, parameters, run command, expected output, and limits.

### Broken root links

#### F06 (Major)
- **File/line:** `README.md:21-31`
- **What is wrong:** Links reference non-existent top-level paths like `./Particles_in_a_Box`, `./MD_Simulations`, `./Ising_Models`.
- **Why it matters:** Front page navigation breaks for users.
- **Suggested fix:** Update links to actual paths (e.g., `./Quantum_Chemistry/Particles_in_a_Box`, `./Classical_Physics/MD_Simulations`, `./Statistical_Mechanics/Ising_Models`).
- **Snippet:**
```md
| [Particles in a Box](./Particles_in_a_Box) |
| [MD Simulations](./MD_Simulations) |
| [Ising Model](./Ising_Models) |
```

### Topic gaps (10 realistic additions, small → big)
1. **Simple Harmonic Oscillator (1D)** — Small
2. **Damped/Driven Pendulum + phase portrait** — Small
3. **Projectile motion with drag** — Small
4. **1D heat equation finite-difference solver** — Small
5. **2D wave equation (membrane)** — Medium
6. **Poisson equation solver for electrostatics (finite difference)** — Medium
7. **Canonical NVT MD (Langevin or Nosé-Hoover thermostat)** — Medium
8. **Lattice gas / 2D percolation criticality** — Medium
9. **Time-dependent Schrödinger (Crank–Nicolson split-step)** — Large
10. **Finite-element or spectral PDE benchmark suite with convergence studies** — Large

---

## Part 2 — Correctness of physics and numerics

#### F01 (Critical)
- **File/line:** `Statistical_Mechanics/Ising_Models/2d_metropolis.py`, `accept(...)` lines 17-46
- **What is wrong:** Energy/sign convention is inverted relative to standard Ising Hamiltonian (`H=-J Σ s_i s_j`), so acceptance rule is effectively reversed.
- **Why it matters:** Violates detailed balance and biases thermodynamic sampling.
- **Suggested fix:** Use `deltaE = E_new - E_old` with consistent Hamiltonian sign and accept if `deltaE <= 0` else with probability `exp(-deltaE/(kT))`.
- **Snippet:**
```python
INITIAL = J * spin * (...)
FINAL   = J * new  * (...)
change = FINAL - INITIAL
if change < 0: return True
```

#### F10 (Major)
- **File/line:** `Statistical_Mechanics/Ising_Models/2d_metropolis.py:96`
- **What is wrong:** `new_E` is printed even if no accepted move assigned it.
- **Why it matters:** Can raise `UnboundLocalError` and terminate run.
- **Suggested fix:** Initialize `new_E = old_E` before loop or print `old_E` after loop.
- **Snippet:**
```python
print(f"Final: {new_E}")
```

#### F15 (Minor)
- **File/line:** `Statistical_Mechanics/Ising_Models/2d_metropolis.py:93-95`
- **What is wrong:** Stops when single-step energy change is tiny (`abs(new_E-old_E)<epsilon`).
- **Why it matters:** Does not indicate thermal equilibration; may stop too early.
- **Suggested fix:** Use burn-in + fixed sweeps and track observables (magnetization/energy autocorrelation).

#### F03 (Major)
- **File/line:** `Quantum_Chemistry/Particles_in_a_Box/Stability_Calculation/1_config.py:68-72`
- **What is wrong:** “Force” accumulator uses derivative of **distance** `r(x)` instead of derivative of LJ potential `U(r(x))`.
- **Why it matters:** Force direction/magnitude are physically incorrect.
- **Suggested fix:** Differentiate `U(r)` w.r.t. coordinate (or use analytical LJ force formula directly).
- **Snippet:**
```python
def f(x):
    return distance(x, ...)
df += numerical_derivative(f, x_data[xi])
```

#### F02 (Critical)
- **File/line:** `Quantum_Chemistry/Particles_in_a_Box/Stability_Calculation/3_stable.py:55,74,85,103`
- **What is wrong:** `dis(...)` is called with wrong arguments (`z_data, [j]`) instead of `z_data[j]`.
- **Why it matters:** Breaks core distance calculations used by energy/force update.
- **Suggested fix:** Replace all `z_data, [j]` with `z_data[j]`.
- **Snippet:**
```python
R = dis(x_data[i], y_data[i], z_data[i], x_data[j], y_data[j], z_data, [j])
```

#### F14 (Major)
- **File/line:** `Quantum_Chemistry/Particles_in_a_Box/` (missing `box.py`)
- **What is wrong:** Requested known suspect file `Particles_in_a_Box/box.py` is absent.
- **Why it matters:** Could not verify force-accumulator overwrite (`=` vs `+=`) issue.
- **Suggested fix:** Add/track `box.py` (or point to replacement file) and include a test asserting pairwise force accumulation.

#### F07 (Major)
- **File/line:** `Learn_Julia/3_boids_algorithm.jl:55-72`
- **What is wrong:** Comment says cohesion moves birds **towards** center of mass, but heading uses vector from COM to bird.
- **Why it matters:** Behavior can oppose intended flock cohesion and confuse learners.
- **Suggested fix:** Use `atan(y_cm - b.y, x_cm - b.x)`.
- **Snippet:**
```julia
# steer to move towards the average position
b.angle += 0.01 * (atan((b.y-y_cm), (b.x-x_cm)) - b.angle)
```

### Sanity-check/test status by simulation
- **MD (velocity Verlet):** No automated energy-drift test; only prints initial/final energy.
  - Proposed check: assert bounded relative energy drift over fixed run.
- **Ising 2D Metropolis:** No validation vs Onsager behavior / Binder cumulant / known `T_c` trend.
  - Proposed check: magnetization decreases sharply near `T≈2.27` (dimensionless units).
- **Logistic map (Python/Julia):** Visual-only.
  - Proposed check: compare period-doubling points against known `r_n` values.
- **Electrodynamics equipotentials:** Visual-only.
  - Proposed check: compare along axis to analytical `V(x)=k(q1/|x|+q2/|x-d|)`.
- **Fourier analysis:** Visual-only.
  - Proposed check: fit numerical FT width/shape against Gaussian analytical transform.
- **Particle-in-box/stability scripts:** No tests.
  - Proposed check: finite-difference force vs analytical LJ force (unit test).
- **QUBO scripts:** No tests.
  - Proposed check: verify objective on small known graph/set-packing instances.
- **Ideal_Electron random walks:** No tests.
  - Proposed check: verify `E[x_n]≈0` and `E[x_n^2]≈n` within tolerance.

---

## Part 3 — Code quality and security

#### F04 (Major)
- **File/line:** `backend.py` missing
- **What is wrong:** Requested security review target file is not in repository.
- **Why it matters:** Cannot verify suspected `subprocess.run` sanitization risk.
- **Suggested fix:** Track backend source (or secure stub) and add tests for command/path sanitization.

#### F09 (Major)
- **File/line:**
  - `Ideal_Electron/Walkplot.py:75`
  - `Ideal_Electron/means.py:60`
  - `Statistical_Mechanics/Monte_Carlo_Methods/estimate_π_MHMC_weak.py:176`
  - `Statistical_Mechanics/Monte_Carlo_Methods/estimate_π_MHMC_strong.py:176`
  - `Statistical_Mechanics/Monte_Carlo_Methods/inverse_transform_sampling_exponential.py:60`
- **What is wrong:** Writes HTML into directories that do not exist in repo.
- **Why it matters:** Runtime `FileNotFoundError`; frontend artifacts are not generated reliably.
- **Suggested fix:** Ensure directory exists (`mkdir -p`) or write to existing tracked output path.
- **Snippet:**
```python
fig.write_html("Ideal_Electron/web_src/means.html")
fig.write_html("Monte_Carlo_Methods/web_src/estimate_pi_MHMC_strong.html")
```

#### F08 (Major)
- **File/line:** `Quantum_Computing/QUBO/Set_Packing.jl:45-46`
- **What is wrong:** Uses `Q` before creation; `build_qubo(...)` result never assigned.
- **Why it matters:** Script cannot execute correctly.
- **Suggested fix:** Call `Q, V_list = build_qubo(V, P)` before `size(Q,1)`.
- **Snippet:**
```julia
n = size(Q, 1)
Q_dict = Dict((i-1, j-1) => Q[i, j] ...)
```

#### F16 (Minor)
- **File/line:** Multiple scripts (e.g., `.../velocity_verlet_simulation.py:215`, `.../2d_metropolis.py:129-132`)
- **What is wrong:** Scripts execute immediately at import.
- **Why it matters:** Hard to test/reuse as modules.
- **Suggested fix:** Wrap entrypoints in `if __name__ == "__main__":` (Python) / functions (Julia).

---

## Part 4 — Scientific computing standards

#### F12 (Major)
- **File/line:** Repo root and Julia dirs (missing files)
- **What is wrong:** No pinned Python dependency file and no Julia environment files.
- **Why it matters:** Results are hard to reproduce across machines.
- **Suggested fix:** Add `requirements.txt` (or `pyproject.toml`) and per-project Julia `Project.toml` + `Manifest.toml`.

#### F13 (Major)
- **File/line:** `.github/workflows/static.yml`
- **What is wrong:** CI only deploys pages; no lint/test workflow.
- **Why it matters:** Regressions are not caught automatically.
- **Suggested fix:** Add minimal CI job for Python syntax/tests and Julia smoke tests.
- **Snippet:**
```yaml
name: Deploy static content to Pages
on:
  push:
    tags:
      - 'v*'
```

#### F17 (Minor)
- **File/line:** Multiple random-sampling scripts (no seed initialization)
- **What is wrong:** Random seeds are not controlled.
- **Why it matters:** Figures/results are non-reproducible.
- **Suggested fix:** Accept optional seed argument and print/store it.

#### F18 (Minor)
- **File/line:** Multiple scripts/readmes
- **What is wrong:** Units are often implied but not systematically documented (SI vs reduced units).
- **Why it matters:** Hard to compare with references or scale to real systems.
- **Suggested fix:** Add explicit unit conventions per script and README.

#### F19 (Minor)
- **File/line:** Repo root
- **What is wrong:** No `CITATION` file.
- **Why it matters:** Harder for users to cite this scientific code correctly.
- **Suggested fix:** Add `CITATION.cff` with authors/version/DOI (if available).

### Julia environment files status (explicit confirmation)
No `Project.toml` or `Manifest.toml` exists in:
- `/Learn_Julia/`
- `/Classical_Physics/Hamiltonian_Chaos/`
- `/Quantum_Computing/QUBO/`
- `/Machine_Learning/Language_Models/`
- `/Machine_Learning/Reinforcement Learning/`
(Also none at repo root.)

### Repo basics check
- `LICENSE`: **Present** (`MIT`)
- `.gitignore`: **Present**
- `CONTRIBUTING.md`: **Present**
- `CITATION*`: **Missing**

---

## 4) Prioritized fix plan

### Do first
1. **Fix Ising Metropolis acceptance/energy sign consistency** (F01, F10) — **Effort: medium**
2. **Fix `3_stable.py` distance-call bug and re-check LJ force logic** (F02) — **Effort: medium**
3. **Track/restore `models.json` and `backend.py` for reviewability and security checks** (F04, F05, F14) — **Effort: small-medium**
4. **Fix broken pathing and output directories (`README` links + `web_src`)** (F06, F09) — **Effort: small**

### Do next
1. **Add dependency management files (Python + Julia envs)** (F12) — **Effort: medium**
2. **Add minimal tests + CI test workflow** (F13) — **Effort: medium**
3. **Correct boids cohesion direction and comments** (F07) — **Effort: small**
4. **Fix QUBO Set Packing execution flow** (F08) — **Effort: small**

### Nice to have
1. **Add missing README docs in all simulation folders** (F11) — **Effort: medium**
2. **Add seeds/unit conventions/citation metadata** (F17, F18, F19) — **Effort: small**
3. **Refactor scripts into importable modules with guarded entrypoints** (F16) — **Effort: medium**

---

## 5) Could not verify
1. **`models.json` registration and frontend reachability** — file is missing from tracked repository.
2. **`backend.py` security issues (including suspected unsanitized `subprocess.run`)** — file is missing from tracked repository.
3. **Known suspect in `Particles_in_a_Box/box.py` (`=` vs `+=` force accumulation)** — `box.py` is not present in repository.
4. **HuggingFace Space wiring/runtime behavior** — no tracked Space app/backend files in this clone to verify end-to-end integration.

