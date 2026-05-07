# Learn Julia
The goal of this folder is to learn julia through scientific computing

## Installing Julia

Use `juliaup` — the official Julia version manager. Do not download from the website directly.

**Linux / macOS**
```bash
curl -fsSL https://install.julialang.org | sh
```

**Windows**
```powershell
winget install julia -s msstore
```

Then install the latest stable version:
```bash
juliaup add release
juliaup default release
```

Verify:
```bash
julia --version
```

---

## The REPL (Read-Eval-Print Loop)

Start it by typing `julia` in your terminal. Four modes:

| Key | Mode | Purpose |
|---|---|---|
| default | Julia | run code |
| `]` | Pkg | manage packages |
| `;` | Shell | run shell commands |
| `?` | Help | documentation |

Exit any mode with `Backspace`. Exit the REPL with `Ctrl+D`.

---

## Setting Up This Project

From inside this folder:

```bash
julia --project=.
```

Then in the REPL, hit `]` to enter Pkg mode and install dependencies:

```julia
] instantiate
```

If starting fresh with no `Project.toml` yet:

```julia
] activate .
] add LinearAlgebra Statistics Plots
```

---

## Editor

VS Code with the [Julia extension](https://www.julia-vscode.org/) is the recommended setup. It gives inline output, a plot pane, and a proper debugger.

Alternatively, Jupyter notebooks work via:
```julia
] add IJulia
```

---

## Running a Simulation

```bash
julia --project=. my_simulation.jl
```

Or from inside the REPL:
```julia
include("my_simulation.jl")
```

`include` is preferred while developing it reuses the same Julia session and avoids recompilation.

---

## Key Packages Used in This Folder

| Package | Purpose |
|---|---|
| `LinearAlgebra` | matrix operations, eigensolvers stdlib, no install needed |
| `Statistics` | mean, std, variance stdlib |
| `Plots` | plotting with multiple backends |
| `DifferentialEquations` | ODE/SDE solvers |

---
