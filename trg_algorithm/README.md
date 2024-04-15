## Tensor Renormalization Group Algorithm

**Mentors:** Peter Majcen, Nora Reinić

### Overview

Renormalization group is a theoretical framework developed to understand the properties of many-body systems in thermodynamic limit. The main idea relies on the assumption that many-body systems at large scales show universal behaviour driven by the collective phenomena, rather than the individual interactions between the constituents. Thus, the aim is to identify and analyise these universal properties which remain unchanged regardless of the scale of the observation.

The mechanism on which the renormalization group analysis is based is coarse-graining the lattice: we gradually map a system of large number of particles into the one of a smaller number of particles, while retaining the a part of information about the bigger system. In this challenge, we focus on is a family of implementations of the renormalization group idea based on the tensor network techniques, and in particular, implementing the Tensor Renormalization Group (TRG) algorithm \cite{Levin2007} for the 2D classical Ising model.


### Tasks

- Understand how to write the partition function of a many-body Ising spin model in 2D as a tensor network
- Implement the TRG algorithm to compute the system's Helmholtz free energy per site
- Determine the critical temperature of the system
- Compare the results with the exact solution and analyse the algorithm's performance in the different Hamiltonian parameter and convergence parameter regimes
- **Optional**: investigate how to compute the system's magnetization
- **Optional**: explore the possible improvements of the TRG algorithm


### Materials

More details and a guide through the main theoretical concepts are in [trg_guide.pdf](trg_guide.pdf).

For comparing the results, there is the [Jupyter Notebook](2D_ising_exact.ipynb) that reproduces the analytical solution of the problem.
