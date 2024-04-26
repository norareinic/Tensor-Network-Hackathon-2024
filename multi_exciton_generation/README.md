## Multi-exciton generation in molecular semiconductors via singlet fission

Excitons are bound electron-hole pair quasiparticles associated with the excited electronic states of a photoactive molecule. A singlet exciton (spin $S=0$) is formed when a molecule absorbs a photon in resonance with the energy difference between ground (no exciton) and excited state (one exciton). Organic solar cells (OSCs) generate a photocurrent by absorbing photons that form excitons in a photoactive molecular layer. The excitons are then transported in the material until they reach an electron acceptor, where they undergo charge separation.

However, the short lifetime ($\approx$ ns) and diffusive transport of singlet excitons limits the efficiency of OSCs. Singlet fission is now being explored as a way to improve the efficiency of organic solar cells. In singlet fission a photo-generated singlet exciton (spin $S=0$) splits into two triplet excitons (each with spin $S=1$) in a energy-conserving and spin-conserving transition. Once the triplets migrate away from each other they become optically dark, leading to longer exciton lifetimes ($\approx$ $\mu$s). This multi-exciton generation process leads to higher efficiency by producing two excitons per absorbed photon, and by increasing the probability for the excitons to reach an electron acceptor due to their longer lifetime.

In this project we will implement a numerical model to study the initial event of singlet fission in extended solids, which remains a challenge in the field. We will begin by considering a simplified model that can be solved analytically and numerically on a small lattice (2 to 10 sites). We will then study the model using symmetric tensor networks (TNs). After comparing the TN results with known solutions, we will scale up the model to consider larger lattices, disorder, and the effect of the vibrational modes of the lattice.

<img src="SpinSC_problem_set_figure.png" alt="drawing" width="80%"/>

**Scientific mentor:** Francesco Campaioli\
**Code mentor:** Alice Pagano

### Tasks

- Following the notes on singlet fission, use [qtealeaves](https://pypi.org/project/qtealeaves/) to implement the singlet fission Hamiltonian and dynamics for 1D rings with $N$ sites (nearest-neighbour couplings and periodic boundary conditions). Ignore the vibrational modes so that each site represents an exciton site. Use symmetric Tree Tensor Networks.

- Study the unitary dynamics of an initial singlet exciton state. Consider the parameters of the *resonant triplet-pair solution* with singlet exciton energy $\varepsilon_S = 1$ (see notes) and initialise the system in the ground state of the singlet exciton Hamiltonian with $n_0 = 1$ singlet in the medium. Propagate this initial state via a quench e compare the results with the solution provided in the jupyter notebook for $N = 4$. 

    - How does the solution change with the `propertymax_bond_dimension`?
    - Does the dynamics change with the number $N$ of sites?

- Implement the function to evaluate singlet fission efficiency over a time interval (see notes) and study the efficiency of singlet fission (i.e., how likely 2$n$ triplets are formed per $n$ initial excitons) as a function of the initial number of singlet excitons $n_0\in(1,N)$.

- Generalise the model by allowing disorder (see code snippet for help) both in the local terms and in the two-body interactions. Study the dynamics of the system with disorder in the triplet hopping coupling $J_T$ and in the triplet-triplet interaction $\chi$, by running multiple trajectories, each with a different realisation of disorder. Only consider one initial singlet in the medium ($n_0=1$). Does disorder improve or worse singlet fission efficiency?

- Extend the model by adding one vibrational mode (phonon) per site (see notes). Embed the excitons and the phonon (which can be modelled as a boson) within the same site (see code snippet for help) and limit the size of the phonon to $n_max = 3$ (`fock_space_nmax=3`). Assume that the phonons relax via the local Lindblad operators $\gamma_- \hat{a}_i$, with $\gamma = 0.1 \varepsilon_S$. Couple the phonon to the excitons only via singlet-phonon interactions with coupling strength $g_S$. Study the dynamics of the system for $N=4$ ignoring disorder, as a function of $g_T$. 

### Material

- Notes on the theoretical formulation of singlet fission in many-body systems.
- A jupyter notebook with the QuTiP implementation of the *resonant triplet-pair solution*, which can be used to compare the TTN results with an exact solution.
- Code snippet to generate different random local and two-body terms over multiplet trajectories.
- Code snippet to implement an exciton-boson site embedding.