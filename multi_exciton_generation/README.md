## Multi-exciton generation in molecular semiconductors via singlet fission

Excitons are bound electron-hole pair quasiparticles associated with the excited electronic states of a photoactive molecule. A singlet exciton (spin $S=0$) is formed when a molecule absorbs a photon in resonance with the energy difference between ground (no exciton) and excited state (one exciton). Organic solar cells (OSCs) generate a photocurrent by absorbing photons that form excitons in a photoactive molecular layer. The excitons are then transported in the material until they reach an electron acceptor, where they undergo charge separation.

However, the short lifetime ($\approx$ ns) and diffusive transport of singlet excitons limits the efficiency of OSCs. Singlet fission is now being explored as a way to improve the efficiency of organic solar cells. In singlet fission a photo-generated singlet exciton (spin $S=0$) splits into two triplet excitons (each with spin $S=1$) in a energy-conserving and spin-conserving transition. Once the triplets migrate away from each other they become optically dark, leading to longer exciton lifetimes ($\approx$ $\mu$s). This multi-exciton generation process leads to higher efficiency by producing two excitons per absorbed photon, and by increasing the probability for the excitons to reach an electron acceptor due to their longer lifetime.

In this project we will implement a numerical model to study the initial event of singlet fission in extended solids, which remains a challenge in the field. We will begin by considering a simplified model that can be solved analytically and numerically on a small lattice (2 to 10 sites). We will then study the model using symmetric tensor networks (TNs). After comparing the TN results with known solutions, we will scale up the model to consider larger lattices, disorder, and the effect of the vibrational modes of the lattice.

![](SpinS_problem_ste_figure.png)

**Scientific mentor:** Francesco Campaioli
**Code mentor:** Alice Pagano

### Tasks

- Adapt the simplified singlet fission model and derive analytical and numerical results, using the notes and the provided QuTiP implementation.
- Implement a scalable simplified model using TNs.
- Benchmark the TN results against theory and exact diagonalisation methods.
- Scale the model up and study singlet fission for larger lattices, disordered materials, and exciton-phonon interactions.

### Materials

