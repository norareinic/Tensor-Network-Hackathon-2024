## Solving MaxCut with  simulated quantum annealing

QUBO problems pose a significant challenge in optimization, falling under the category of NP-hard problems with diverse applications spanning from finance to machine learning. These problems can be effectively translated into a ground state search for an Ising Hamiltonian and subsequently addressed through quantum annealing. We tackle a QUBO problem by simulating a suitable quantum annealing process using a TN ansatz.

**Mentors:** Davide Rattacaso

### Tasks

- Map a max-cut problem to a QUBO problem and solve it with a brute-force algorithm.
- Map a QUBO problem to ground state search and solve with quantum annealing (exact simulation).
- Map a larger QUBO problem to ground state search and solve by simulating quantum annealing with TN.  Which class of graphs is more suitable for the TN ansatz?
- Investigate how the capability of finding low energy states depends on the bond dimension, the annealing time and, the number of steps in the TDVP evolution, and the features of the MaxCut graph (e.g., average connectivity and topology).
- Use OPES sampling for studying how the energy distribution evolves during the process.
- Compare the performances of quantum annealing and variational GS search.



### Materials

- A guide through the main theoretical concepts are in [max_cut_qa_guide.pdf](max_cut_qa_guide.pdf).
- A minimal example where quantum annealing is simulated with Quantum TEA is in the jupyter notebook [quantum_annealing_simulation.ipynb](quantum_annealing_simulation.ipynb).

