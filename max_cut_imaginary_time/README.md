## Solving MaxCut with TN imaginary time evolution

QUBO problems pose a significant challenge in optimization, falling under the category of NP-hard problems with diverse applications spanning from finance to machine learning. These problems can be effectively translated into a ground state search for an Ising Hamiltonian. We tackle a QUBO problem by simulating imaginary time evolution of an initial superposition of all possible configurations driven by the associated Ising Hamiltonian. We exploit TN imaginary time TDVP to scale up the optimization to large QUBO instances.

**Mentors:** Davide Rattacaso

### Tasks

- Map a MaxCut problem to a QUBO problem and solve it with a brute-force algorithm.
- Solve a MaxCut problem with imaginary time evolution (exact simulation).
- Solve a large MaxCut by simulating imaginary time evolution with TN. Which class of graphs is more suitable for the TN ansatz?
- Investigate how the capability of finding low energy states depends on the bond dimension and the features of the MaxCut graph (e.g., average connectivity and topology).
- Use OPES sampling for studying how the energy distribution evolves during the process.
- Compare the performances of imaginary-time evolution and variational GS search.


### Materials

- A guide through the main theoretical concepts are in [max_cut_it_guide.pdf](max_cut_it_guide.pdf).
- A minimal example where imaginary time evolution is simulated with Quantum TEA is in the jupyter notebook [quantum_annealing_simulation.ipynb](imag_time_simulation.ipynb).

