# This code is part of qmatchatea.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

r"""
Execute a single circuit on multiple processes with MPI
=======================================================

In this example, we prepare a simple quantum circuit that
can be executed parallely on multiple processes. This means
that the MPS state is going to be divided between the different
processes, and each one of the processes will apply gates to
its subsystem.
At the end of the circuit, all the MPS will be gathered on
the rank 0 process to perform the measurement of the observables.

NOTICE: differently from `data_parallelism_mpi_example.py` this example
is not employing data parallelism: you are really executing a single
quantum circuit in parallel!

It is important to run this script as you would run an MPI process, to
enable the use of MPI communications. The correct way of launching the
example is:

.. codeblock::

    mpiexec -n 2 python3 mpi_mps.py

where the ``-n`` parameters indicates the number of processes you use.
"""

import numpy as np
import matplotlib.pyplot as plt
import qtealeaves.observables as obs
from qmatchatea import QCConvergenceParameters, QCBackend, run_simulation
from qmatchatea.utils import MPISettings
from qiskit import QuantumCircuit
from qtealeaves.emulator import MPS

# Try to import mpi4py and exit the program if it is not installed.
# This procedure is done to allow sphinx-gallery to compile all the
# examples
try:
    from mpi4py import MPI
except ImportError:
    print("Program is not being executed due to mpi4py not being installed")
    exit(0)

###############################################################################
# Preparing the circuit.
# Here we go for something simple:
# 1) A layer of Hadamard;
# 2) A layer of random Rz rotations;
# 3) A layer of CNOTs on even qubits;
# 4) A layer of CNOTs on odd qubits.
#
# We repeat `num_layers` times 2)-4). This circuit structure is an optimal
# structure to parallelize, since all the gates can, in principle, be executed
# in parallel


def apply_layer(qc):
    """
    Apply a layer as defined in the comments 2)-4) to a quantum
    circuit

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit where to apply the layer

    Returns
    -------
    QuantumCircuit
        The modified quantum circuit
    """
    # Apply random Z rotations
    for ii in range(qc.num_qubits):
        qc.rz(np.random.uniform(0, 2 * np.pi), ii)
    # Apply even cnots
    for ii in range(0, qc.num_qubits - 1, 2):
        qc.cx(ii, ii + 1)
    # Apply odd cnots
    for ii in range(1, qc.num_qubits - 1, 2):
        qc.cx(ii, ii + 1)
    return qc


def main():
    num_qubits = 16
    num_layers = 30
    np.random.seed([11, 13, 23, 41])
    qc = QuantumCircuit(num_qubits)

    # Apply hadamard
    for ii in range(num_qubits):
        qc.h(ii)
    # Apply the layers
    for _ in range(num_layers):
        apply_layer(qc)

    ###############################################################################
    # Define the observables we are interested in. In this case we are interested
    # in the final statevector, so we save the state, and projective measurements.

    observables = obs.TNObservables()
    observables += obs.TNObsProjective(128, True)
    observables += obs.TNState2File("state", "U")

    ###############################################################################
    # Define the convergence parameters, in particular the maximum bond dimension.
    # The maximum bond dimension controls how much entanglement we can encode in
    # the system while still obtaining trustful results.
    # The maximum bond dimension reachable for a given number of qubits :math:`n`
    # is :math:`\chi=2^{\lfloor\frac{n}{2}\rfloor}`. As you see, if we want to
    # encode *any* state we still have an exponential scaling.
    # However, we have ways to understand if the results of our computations are
    # meaningful, through the analysis of the singular values cut through the
    # simulation.
    conv_params = QCConvergenceParameters(
        max_bond_dimension=2 ** (num_qubits // 2), trunc_tracking_mode="C"
    )

    ###############################################################################
    # We set `num_procs=1` because the `num_procs` is a fortran-only parameter. The
    # number of processes for this script is set when the program is launched.
    # The MPI approach is set to "CT", where the MPS is diveded among different
    # processes. I.e., if we have 4 qubits and 2 processes, the first process
    # will handle qubits 0,1 and the second 2, 3. Communications will happen when
    # operations are done on qubit 1, 2.
    # The approach "SR" is instead a normal serial application of the algorithm

    # The most important part for you is here, in the isometrization parameter.
    # A negative isometrization is equivalent to a serial step.
    # A positive isometrization is equivalent to a parallel step with n layers
    # A list is accessed with periodic boundary condition for the different isometrization
    # steps
    mpi_settings = MPISettings(mpi_approach="CT", isometrization=-1, num_procs=1)
    backend = QCBackend(
        backend="PY", precision="Z", device="cpu", mpi_settings=mpi_settings
    )

    results = run_simulation(
        qc,
        convergence_parameters=conv_params,
        observables=observables,
        backend=backend,
        where_barriers=3,  # we apply a reisometrization every 3 layers
    )

    # Print results only if we are on rank 0
    if MPI.COMM_WORLD.Get_rank() == 0:
        print(f"Used {MPI.COMM_WORLD.Get_size()} processors")
        print(f"Time spent for parallel simulation: {results.computational_time}s")

        # We also run the simulation serially to compare the results
        mpi_settings = MPISettings(mpi_approach="SR", isometrization=-1, num_procs=1)
        backend = QCBackend(
            backend="PY", precision="Z", device="cpu", mpi_settings=mpi_settings
        )

        observables = obs.TNObservables()
        observables += obs.TNObsProjective(128, True)
        observables += obs.TNState2File("state_serial", "U")
        results_serial = run_simulation(
            qc,
            convergence_parameters=conv_params,
            observables=observables,
            backend=backend,
        )
        print(f"Time spent for serial simulation: {results_serial.computational_time}s")

        # Load the MPS states to check for the results
        mps1 = MPS.from_tensor_list(np.load("data/out/state.pklmps", allow_pickle=True))
        mps2 = MPS.from_tensor_list(
            np.load("data/out/state_serial.pklmps", allow_pickle=True)
        )
        print(
            f"Fidelity of the parallel result: { np.abs(mps1.contract(mps2))**2 }. Expected result is 1."
        )


if __name__ == "__main__":
    main()
