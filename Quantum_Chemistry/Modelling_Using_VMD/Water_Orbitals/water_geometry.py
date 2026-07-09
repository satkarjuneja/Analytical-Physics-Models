import psi4

psi4.set_memory('2 GB')
psi4.core.set_output_file('output.dat', False)

# Geometry
mol = psi4.geometry("""
0 1
O
H 1 0.96
H 1 0.96 2 104.5
""")

# Set options
psi4.set_options({
    'basis': 'cc-pVDZ',
    'scf_type': 'df'
})

# Run SCF
energy, wfn = psi4.energy('scf', return_wfn=True)


print("Dipole:", wfn.variable("SCF DIPOLE"))

