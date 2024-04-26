## Hard Optimization with Tensor Networks: The Knapsack Problem

Optimization problems arise in various disciplines and scenarios, spanning almost every scientific domain. Essentially, these problems involve the search for the best solution among a set of viable alternatives, with the overarching goal of improving efficiency, performance, or understanding within a specific context.

Within this setting, the Knapsack Problem (KP) is one of the simplest non-trivial binary models that describes a wide range of practically relevant optimization problems, ranging from economic-financial investment decision-making, planning of missions for data acquisition by a group of satellites in the field of Earth Observation, to logistics tasks in cargo transportation.

The KP involves selecting, from a list of items, a subset of these, with the goal of maximazing the total profit while respecting a capacity constraint. One possible interpretation of the problem is the preparation of a mountaineer's backpack for a mountain hike: among the numerous desired items, each characterized by a weight that increases the backpack load once the item is chosen, and by a benefit or profit that measures the utility or comfort provided by the item when carried. For obvious reasons, the mountaineer wants to limit the total weight of his backpack and therefore sets the maximum load with the capacity value. At the same time, he wants to maximize the benefit provided by the selected items.

In this project, we address this NP-hard challenge by implementing the Quantum Approximate Optimization Algorithm (QAOA). The objective is to explore the potential benefits of this quantum optimization approach compared to state-of-the-art classical algorithms. Furthermore, we use Tensor Network (TN) methods to simulate larger instances of the KP, enabling us to evaluate the performance of QAOA on larger problems.

**Mentor:** Marco Tesoro

### Tasks

- Understand how to map a constrained optimization problem into a Quadratic Unconstrained Binary Optimization (QUBO) form;
- Understand the equivalence between QUBO and a classical Ising model with long-range random interactions;
- Implement the mapping from the QUBO reformulation of the KP onto a quantum many-body Hamiltonian;
- Implement the QAOA using the [Qiskit](https://docs.quantum.ibm.com/api/qiskit/0.45) quantum software.
- Apply QAOA to determine the ground state and explore the quality of the encoded KP solution in different circuit parameter regimes.
- Leverage TN and HPC resources to address larger instances of the KP.
- Compare QAOA solutions with classical approaches.
- **Optional**: investigate how to improve the circuit parameters initialization (??????????).
- **Optional**: explore variants and improvements of QAOA (?????????????).

### Materials

- The mathematical formulation of the KP as a binary linear integer program and the process of mapping solutions to it in the ground-state search of a many-body Hamiltonian can be found in [qubo_guide.pdf](qubo_guide.pdf).
- More details and a guide through the main theoretical concepts of QAOA algorithm are in [name_guide.pdf](name_guide.pdf).
- Code snippet for generating the QUBO given a KP instance are in []()........
- For comparing the results with brute-force approach and state-of-the-art classical solver, there is the [Jupyter Notebook](kp_classical_solvers.ipynb) that can be used as a starting point on the generated KP instances.