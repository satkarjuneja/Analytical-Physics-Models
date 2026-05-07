import psi4

# Memory and threads
psi4.set_memory('8 GB')
psi4.set_num_threads(4)

# Molecule: benzene (C6H6)
c6h6 = psi4.geometry("""
0 1
C      0.0000    1.3960    1.0000
C      1.2096    0.6980    1.0000
C      1.2096   -0.6980    1.0000
C      0.0000   -1.3960    1.0000
C     -1.2096   -0.6980    1.0000
C     -1.2096    0.6980    1.0000
H      0.0000    2.4790    1.0000
H      2.1470    1.2400    1.0000
H      2.1470   -1.2400    1.0000
H      0.0000   -2.4790    1.0000
H     -2.1470   -1.2400    1.0000
H     -2.1470    1.2400    1.0000
""")

# Set basis
psi4.set_options({'basis': '3-21g'})

# Compute Hartree-Fock energy
energy_hf = psi4.energy('scf', molecule=c6h6)
print("Hartree-Fock energy (C6H6):", energy_hf)

