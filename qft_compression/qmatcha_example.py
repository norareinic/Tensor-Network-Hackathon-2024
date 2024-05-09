r"""
Saving the final state
======================

All the examples in the `examples/observables/` folder have the same initial
structure, where we define the state, the IOinfo and the backend.
What changes is **only** what we measure.
While there is an example **for each observable** you can measure multiple
observables in the same operations, as shown in other examples.

The state we generate with a quantum circuit, and on which we will run all
the observables, is a GHZ state on `n=100` qubits.
This is a "good" state for tensor network simulations because it can be
represented with a bond dimension :math:`\chi=2`.
The GHZ state is as follows:

.. math::

  |\psi\rangle = \frac{1}{\sqrt{2}} ( |00...0\rangle + |11...1\rangle)

In this example, we show how to save the tensor network state to file.
This can be really useful for long simulations, to measure further
observables in another time. There are two possibilities for saving
the TN state:

- "U", unformatted. This will save the tensor network in a binary format,
  that can be read only by specific tools;
- "F", formatted. This will save the tensor network as a plain text file.
  While easier to distribute, this is less optimized.

"""

# Import necessary modules
import numpy as np
from qiskit import QuantumCircuit
from qtealeaves.observables import TNState2File, TNObservables
from qmatchatea import run_simulation, QCIO
from qmatchatea.utils.qk_utils import GHZ_qiskit
from qmatchatea.utils.utils import print_state


def main():
    # Write down the quantum circuit. This GHZ state given by the qmatcha library is the "best"
    # for MPS tensor networks, since it uses a linear connectivity
    num_qubits = 10
    qc = QuantumCircuit(num_qubits)
    _ = GHZ_qiskit(qc)

    ################################################################################
    # QCIO is the class devoted to handle the IO of a qmatchatea simulation.
    # Specifically, it is going to create a folder where the identifiers of the
    # simulation are saved, or where the results are saved. On top of that,
    # through the IO you can define an initial state which is not |00...0>

    io_info = QCIO(inPATH="data/in/", outPATH="data/out/", initial_state="vacuum")

    ################################################################################
    # We can then add the specific observable to the class :py:class:`TNObservables`,
    # which is the one devoted to the input/output/measurement management.
    # Notice that all the observables are actually defined in qtealeaves.

    observables = TNObservables()

    ################################################################################
    # The observable for saving the final state. You can specify the filename,
    # and the state will be saved in your output directory + filename.
    # The file extension is added automatically.

    save_state = TNState2File(name="my_tn_state", formatting="U")
    observables += save_state

    ################################################################################
    # Now we run the simulation passing all the parameters seen in this example.
    # There are many more parameters available that are set as default here!

    results = run_simulation(qc, observables=observables, io_info=io_info)

    ################################################################################
    # Using the load_state method we load the file we previously saved with
    # TNState2File, and it will be saved in `observables["tn_state"], also
    # retrievable with `results.tn_state`

    results.load_state()

    ################################################################################
    # To retrieve the bond entropy observables, access the results.entanglement
    # The result is a dict, where the key is the bipartition and the value the
    # entanglement value. In case of a GHZ, all the bipartitions have the same
    # entanglement. Thus, we will only look at a random bipartition.
    # The results in this case are lists, where the results idx corresponds to
    # the qubit idx. For a GHZ state, all the qubits give the same result, so we
    # just take a random index

    state = results.observables["tn_state_path"]

    print("-" * 30, "Observables results", "-" * 30)
    print(f"The state is saved in {state}, expected is data/out/my_tn_state.pklmps")
    print(f"Class of the saved TN result is {results.tn_state}")
    print("The resulting statevector is:")
    print_state(results.tn_state.to_statevector(qiskit_order=True).elem )
    print()

    ################################################################################
    # There are some other runtime statistics saved by qmatchatea:
    #
    # - results.computational_time. The time spent in the circuit simulation in
    #   seconds. Available for both python and fortran;
    # - results.observables["measurement_time"]. Time spent in the measurement
    #   process in seconds. Available only in python;
    # - results.observables["memory"]. Memory used during the circuit simulation
    #   in Gigabytes. It is a list of values. Here we just look at the memory peak,
    #   i.e. its maximum. Available only in python;
    # - results.fidelity. Lower bound on the fidelity of the state
    # - results.date_time. yy-mm-dd-hh:mm:ss of the simulation

    comp_time = np.round(results.computational_time, 3)
    meas_time = np.round(results.observables.get("measurement_time", None), 3)
    memory = np.round(np.max(results.observables.get("memory", [0])), 4)
    print("-" * 30, "Runtime statistics", "-" * 30)
    print(f"Datetime of the simulation: {results.date_time}")
    print(f"Computational time: {comp_time} s")
    print(f"Measurement time: {meas_time} s")
    print(f"Maximum memory used: {memory} GB")
    print(
        f"Lower bound on the fidelity F of the state: {results.fidelity}, i.e.  {results.fidelity}≤F≤1"
    )


if __name__ == "__main__":
    main()
