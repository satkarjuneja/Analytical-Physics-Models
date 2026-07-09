import psi4
import numpy as np
import matplotlib.pyplot as plt

psi4.set_memory('2 GB')
psi4.core.set_output_file('output.dat', False)

psi4.set_options({
    'basis': '6-31G*',
    'scf_type': 'df'
})

R_values = np.linspace(0.7, 2.0, 80)
energies = []
energies2 = []


for R in R_values:
    mol = psi4.geometry(f"""
    0 1
    O
    H 1 {R}
    H 1 0.96 2 104.5
    """)
    
    psi4.core.clean()
    E = psi4.energy('scf')
    E2=psi4.energy('mp2')
    energies.append(E)
    energies2.append(E2)

diff=np.array(energies)-np.array(energies2)
# plt.plot(R_values, energies)
# plt.plot(R_values,energies2)
plt.plot(R_values,list(diff))


plt.xlabel("O-H bond length (Å)")
plt.ylabel("HF Energy (Hartree)")
plt.grid(True)
plt.show()
