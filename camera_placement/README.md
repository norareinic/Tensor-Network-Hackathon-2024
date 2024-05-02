## Optimizing Camera Placement for Emergency Prevention and Response

The goal of this project is to apply a tensor-network (TN) approach to a combinatorial optimization problem of industrial interest, the Camera Placement problem, and to estimate the scaling towards realistic problem sizes.

Hyper-spectral cameras can be deployed to monitor a territory to identify signatures of an imminent extreme natural event, such as floods, earthquakes, and wildfires. Depending on the nature of the risk, this kind of systems can also be equipped with sensors to monitor air parameters and seismic activity. The utility of these monitoring systems extends to the emergency response phase, in which it allows to collect useful information to the rescuers, ensuring efficient and swift Search \& Rescue operations. Since this kind of high-resolution and hyper-spectral cameras is very expensive, a limited number of them is available to be deployed. Usually, this number is much smaller than the number of candidate sites.

In this project, we propose an Ising formulation of the Camera Placement Problem similar to that introduced in [1], which is a proxy to real-world applications. Specifically, the problem amounts to finding the optimal placement of the cameras on several available sites. The cameras must be distributed on the territory at optimal locations to maximize the coverage and to reduce overlaps between the field-of-vision of the cameras. This Ising problem will be provided in two variants: a model with sparse connectivity between the sites, in which the number of cameras is not fixed, and a model with full connectivity, due to the soft constraint on the camera number. Since the problem is already in the Ising form, its solution can readily be obtained with a ground state search of the corresponding quantum Hamiltonian.

**Mentors:** Matteo Vandelli, Marco Ballarin

### Tasks

- Understand how to write the partition function of a many-body Ising spin model in 2D as a tensor network
- Implement the TRG algorithm to compute the system's Helmholtz free energy per site
- Determine the critical temperature of the system
- Compare the results with the exact solution and analyse the algorithm's performance in the different Hamiltonian parameter and convergence parameter regimes
- **Optional**: investigate how to compute the system's magnetization
- **Optional**: explore the possible improvements of the TRG algorithm

### Materials

[1] Vandelli, Matteo, et al. "Beyond Theory: Evaluating the Practicality of Quantum Optimization Algorithms for Prototypical Industrial Applications." arXiv preprint arXiv:2311.11621 (2023).

[2] Jupyter notebook for the problem generation (i.e. the Hamiltonian)

[3] Example of how to use [qtealeaves](https://baltig.infn.it/quantum_tea_leaves/py_api_quantum_tea_leaves) to perform a [ground state search or an imaginary time evolution](spinglass_example.py) with spin-glass problems;
