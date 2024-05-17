## Parallel scaling of tensor networks

Analyse the parallel scaling of tensor networks, either for quantum circuits
or for variational searches.

Running tensor network simulations on multiple processes is a challenging task. While
the algorithm might be trivial to parallelize, one of the main features of TN algorithm
is intrinsically serial: the isometry center. It is however possible to "mimic" the isometry
center working with the so-called Vidal form of MPS. From now on, we will only work with MPS.
However, all the properties of having an isometry center, such as the fact that an optimally-local
approximation is also the globally optimal one, are gone.
For this reason, every $L$ layers of the algorithm you need to reisometrize the tensor network.
You have two possibilities:

1. Serial reisometrization. You start from right end of the chain. We right canonize the MPS
   in that process, communicate the boundaries to the next process, and right canonize that process.
   We iterate until we hit the left boundary.
2. Parallel isometrization  [1]. We apply identity gates for $L'$ layers, where a layer is
   an application of 2-qubits identities on all even(odd) qubits. In this way the isometry is exactly
   recovered after $L'=n/2$, where $n$ is the number of qubits. But also $L'<n/2$ might be good enough.

In this project, you will have to address the parallel scaling of the parallel MPS algorithm. With parallel
scaling we denote the speedup of the parallel algorithm over the serial algorithm, that, for reasonable sizes
of the system, should be $O(n)$.

**Mentors**: Marco Ballarin, Gabriella Bettonte

### Tasks

- Test the parallel implementation of MPS quantum circuits using mpi4py up to 16 qubits.
  Use a bond dimension χ = 64. Use different types of circuits: construction of a GHZ
  state, brickwall random circuit in 1d. Are the results correct?
- The MPS state needs to be reisometrized any L layers. After how many layers of the
   brickwall quantum circuit you need to reisometrize? For which number of cycles the
   parallel reinstation of the isometry introduced in [7] is faster than the serial reinstanti-
   ation of the isometry?
- Test the parallel scaling of trotterized ising model evolution
- Test the parallel scaling of a QFT algorithm

### Resources

[1] R.-Y. Sun, T. Shirakawa and S. Yunoki, Improved real-space parallelizable matrix-product
state compression and its application to unitary quantum dynamics simulation, arXiv
preprint arXiv:2312.02667 (2023).

[2] The latest version (1.0.1) of quantum matcha TEA can be installed with `pip install qmatchatea` or directly downloaded from
    the [gitlab repository](https://baltig.infn.it/quantum_matcha_tea/py_api_quantum_matcha_tea).

[3] For an example of how to run a parallel algorithm with quantum matcha TEA see the [python script](mpi_example.py).
