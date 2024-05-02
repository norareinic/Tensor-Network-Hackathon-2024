# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Ground state simulation of a spin-glass model.
==============================================

Example contains the ground state of the spin-glass, conversion from TTN to MPS,
and sampling.

"""
import numpy as np
import matplotlib.pyplot as plt
import qtealeaves as qtl
import qtealeaves.emulator as qtltn
from qtealeaves import modeling


def main(tn_type=5, ite=False):
    """
    Main method for the ground state simulation of 1d spin glass model. Spin
    glass models usually do not conserve any symmetry.

    **Arguments**

    tn_type : int, optional
        Choose 5 for python-TTN, 6 for python-MPS.
        Default to 5.
    ite : bool, optional
        If True, use imaginary time evolution. Otherwise variational ground state search.
        Default to False

    """
    # Set seed for random number generator
    np.random.seed([11, 13, 17, 19])

    # For the spin glass, we have to fix the system size in the moment
    system_sizes = [8]
    get_xrand = lambda params: np.random.rand(params["L"], params["L"])
    get_zrand = lambda params: np.random.rand(params["L"])

    input_folder = lambda params: "SG1d/input_%03d" % (params["L"])
    output_folder = lambda params: "SG1d/output_%03d" % (params["L"])
    ttn_file = lambda params: "SG1d/ttn_gs_%03d" % (params["L"])

    model = modeling.QuantumModel(1, "L", name="SpinGlass")
    model += modeling.RandomizedLocalTerm("sz", get_zrand)
    # Here the interaction is XX. You might need a different interaction for classical problems
    model += modeling.TwoBodyAllToAllTerm1D(["sx", "sx"], get_xrand)

    if ite:
        my_conv = qtl.convergence_parameters.TNConvergenceParameters(
            max_iter=50,             # Maximum number of iterations in the ground state search
            max_bond_dimension=20,
            statics_method=5         # Single-tensor update with imaginary time evolution
        )
    else:
        my_conv = qtl.convergence_parameters.TNConvergenceParameters(
            max_iter=7,             # Maximum number of iterations in the ground state search
            max_bond_dimension=20,
            statics_method=2        # Single-tensor update with space-link expansion
        )
    my_ops = qtl.operators.TNSpin12Operators()

    my_obs = qtl.observables.TNObservables()
    my_obs += qtl.observables.TNState2File(ttn_file, "F")

    simulation = qtl.QuantumGreenTeaSimulation(
        model,
        my_ops,
        my_conv,
        my_obs,
        tn_type=tn_type,
        tensor_backend=2,
        folder_name_input=input_folder,
        folder_name_output=output_folder,
        has_log_file=False,
        store_checkpoints=False,
    )

    params = []
    for system_size in system_sizes:
        params.append({"L": system_size})

    simulation.run(params, delete_existing_folder=True)

    mps_conv_params = qtl.convergence_parameters.TNConvergenceParameters(
        max_bond_dimension=16
    )

    for elem in params:
        ttn_filename = simulation.get_static_obs(elem)[ttn_file(elem)]
        psi_ttn = qtltn.TTN.read(ttn_filename, qtl.tensors.TensorBackend())
        psi_mps = qtltn.MPS.from_tensor_list(
            psi_ttn.to_mps_tensor_list(conv_params=mps_conv_params)[0],
            conv_params=mps_conv_params,
        )

        nsamples = 10
        bound_probabilities = psi_mps.meas_unbiased_probabilities(nsamples)

        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        accumulated = 0.0
        for sample, bounds in bound_probabilities.items():
            accumulated += bounds[1] - bounds[0]
            ax1.fill_between(bounds, [0, 0], [1, 1], label=sample)

        ax1.set_ylim([0, 4])
        ax1.set_xlabel("Probability interval")
        ax1.set_yticks([])
        fig.legend(loc="center", ncol=3)
        plt.savefig("SG1d/samples_L%03d.pdf" % (elem["L"]))

        print(
            "Accumulated probability of %d" % (len(bound_probabilities))
            + " samples: %2.6f" % (accumulated)
            + " (L=%d)" % (elem["L"])
        )

    print(
        f"\nExample `{__file__}` ran successfully; "
        + "pdf-plots are saved to SG1d folder; "
        + "no asserts implemented."
    )

    return


if __name__ == "__main__":
    main(ite=False)
