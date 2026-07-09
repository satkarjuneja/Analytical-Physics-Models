import psi4
import numpy as np

# Memory and output
psi4.set_memory('2 GB')
psi4.core.set_output_file('output.dat', False)

# Basis set
psi4.set_options({'basis': 'sto-3g'})

# Geometry (water)
mol = psi4.geometry("""
0 1
symmetry c1
O
H 1 0.96
H 1 0.96 2 104.5
""")


# Run SCF and return wavefunction
energy, wfn = psi4.energy('scf', return_wfn=True)

print(f"SCF Energy: {energy:.10f} Hartree")

# Number of alpha electrons
nalpha = wfn.nalpha()

# Orbital indices (0-based)
homo = nalpha - 1
lumo = nalpha

# Orbital energies (Hartree)
eps = np.array(wfn.epsilon_a())

print(f"HOMO index: {homo}")
print(f"LUMO index: {lumo}")
print(f"HOMO energy: {eps[homo]:.6f} Hartree")
print(f"LUMO energy: {eps[lumo]:.6f} Hartree")
print(f"Gap: {eps[lumo] - eps[homo]:.6f} Hartree")

# Generate cube files
psi4.cubeprop(
    wfn,
    cubeprop_tasks=['orbitals'],
    cubeprop_orbitals=[homo, lumo]
)
