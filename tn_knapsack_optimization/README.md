## Hard Optimization with Tensor Networks: The Knapsack Problem

Optimization problems arise in various disciplines and scenarios, spanning almost every scientific domain. Essentially, these problems involve the search for the best solution among a set of viable alternatives, with the overarching goal of improving efficiency, performance, or understanding within a specific context.

Within this setting, the Knapsack Problem (KP) is one of the simplest non-trivial binary models that describes a wide range of practically relevant optimization problems, ranging from economic-financial investment decision-making, planning of missions for data acquisition by a group of satellites in the field of Earth Observation, to logistics tasks in cargo transportation.

The KP involves selecting, from a list of items, a subset of these, with the goal of maximazing the total profit while respecting a capacity constraint. One possible interpretation of the problem is the preparation of a mountaineer's backpack for a mountain hike: among the numerous desired items, each characterized by a weight that increases the backpack load once the item is chosen, and by a benefit or profit that measures the utility or comfort provided by the item when carried. For obvious reasons, the mountaineer wants to limit the total weight of his backpack and therefore sets the maximum load with the capacity value. At the same time, he wants to maximize the benefit provided by the selected items.

In this project, we address this NP-hard challenge by implementing the Quantum Approximate Optimization Algorithm (QAOA). The objective is to explore the potential benefits of this quantum optimization approach compared to state-of-the-art classical algorithms. Furthermore, we use Tensor Network (TN) methods implemented in *qmatchatea* to simulate larger instances of the KP, enabling us to evaluate the performance of QAOA on larger problems.

**Mentor:** Marco Tesoro

### Tasks

1) Implement a brute-force algorithm to solve small instances of the KP and gain insight into its limitations;
2) Understand how to map a constrained optimization problem into a Quadratic Unconstrained Binary Optimization (QUBO) form
3) Understand the equivalence between QUBO and a classical Ising model with long-range random interactions
4) Implement the mapping from the QUBO reformulation of the KP onto a quantum many-body Hamiltonian
5) Implement the QAOA using the [Qiskit](https://docs.quantum.ibm.com/api/qiskit/0.45) quantum software
6) Apply QAOA to determine the ground state and explore the quality of the encoded KP solution in different circuit parameter regimes
7) Leverage *qmatchatea* and HPC resources to address larger instances of the KP
8) Compare QAOA solutions with classical approaches, using the exact brute-force algorithm for smaller instances and the the CPLEX BILP classical solver for larger instances;
9) **Optional**: investigate how to improve the QAOA circuit variational parameters initialization;
10) **Optional**: explore variants and improvements of QAOA.

### Materials

- The mathematical formulation of the KP as a QUBO problem and the process of mapping its solutions into the ground-state search of a many-body Hamiltonian can be found in [kp_qubo_guide.pdf](kp_qubo_guide.pdf);
- Qiskit tutorial on QAOA can be found [here](https://qiskit-rigetti.readthedocs.io/en/v0.4.1/examples/qaoa_qiskit.html) and [here](https://learning.quantum.ibm.com/tutorial/quantum-approximate-optimization-algorithm);
- The latest version (1.1.x) of quantum matcha TEA can be installed with `pip install qmatchatea` or directly downloaded from the [gitlab repository](https://baltig.infn.it/quantum_matcha_tea/py_api_quantum_matcha_tea).
- We provide three sets of hard KP instances in the [kp_instances](kp_instances) folder, categorized by size: small, medium, and large. Use the small instances set to test the brute-force approach and verify your QAOA implementation. For scaling QAOA with quantum matcha TEA, use the medium and the large folders. Every subfolder contains 24 instances at fixed size and varying profits, weights and capacity. The first line of this file represents the number of items, $ n $. Each of the $ n $ following lines describe an item and contains $ 3 $ integers: the <em>id</em> of the item starting from $ 0 $, the <em>profit</em> of the item and its <em>weight</em>. The last line contains an integer describing the knapsack capacity $ \mathcal{C} $;
- To compare the results of brute-force and quantum (exact, QAOA, matcha TEA) approaches with a state-of-the-art classical solver, we provide a [Jupyter Notebook](benchmarking.ipynb). This notebook includes a cell for loading a KP instance from the instances folder, and another cell that implements the entire workflow for using the [CPLEX solver](https://docs.quantum.ibm.com/api/qiskit/0.24/qiskit.optimization.algorithms.CplexOptimizer) provided by Qiskit;
- Finally, the file [requirements.txt](requirements.txt) can be used to install the necessary Python packages along with their corresponding compatible versions for the project. To install the packages run `pip3 install -r requirements.txt`.
