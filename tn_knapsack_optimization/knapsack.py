##############################################################################
#                              COPYRIGHT NOTICE                              #
##############################################################################
#
# This code is part of the Tensor Network Hackathon
# project of the Quantum Padova group.
# (https://baltig.infn.it/qpd/tensor-network-hackathon)
#
# This code is licensed under the Apache License, Version 2.0.
# You may obtain a copy of this license at 
# http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
#
# The original code is provided by Marco Tesoro.
#
##############################################################################
##############################################################################


## Modules
from random import seed, randint
from math import pow, log2, floor
from numpy import triu, zeros, diagonal, dot as npdot, sum as npsum


## Knapsack Problem: instances generator
def kp_instance(n_items,
                max_capacity,
                classes=2,
                fraction=0.1,
                epsilon=0,
                small=10,
                instance_id=""):

    ### Conditions on the parameters
    if classes < 2:
        raise ValueError(
            "The classes parameter of the generator must be greater than 1."
            )
    if not (0 <= fraction <= 1):
        raise ValueError(
            "The fraction parameter of the generator must be in [0, 1]."
            )
    if small >= max_capacity:
        raise ValueError(
            "The upper bound for profits and weights"
            " must be smaller than the knapsack capacity"
            )

    ### Initializing
    seed(1)
    amountCtr = 0
    total_weight = 0
    denominator = 2.0
    amountSmall = int(n_items * fraction)
    am1 = (n_items - amountSmall) // classes
    filename = f"kp_instance_n_{n_items}_C_{max_capacity}" + instance_id
    
    ### Generating the KP random instance
    with open(filename, 'w') as out_file:
        print(n_items, file=out_file)
        for gg in range(classes):
            for ii in range(am1):
                num1 = randint(1, small)
                num2 = randint(1, small)
                pj = (int)((1/denominator + epsilon) * max_capacity + num1)
                wj = (int)((1/denominator + epsilon) * max_capacity + num2)
                if wj > max_capacity:
                    raise ValueError(
                        "Non-triviality condition on"
                        " individual weight violated"
                        )
                total_weight += wj
                print(amountCtr, " ", pj, " ", wj, file=out_file)
                amountCtr+=1
            denominator*=2
        for jj in range(amountCtr, n_items):
            num1 = randint(1, small)
            num2 = randint(1, small)
            total_weight += num2
            print(jj, " ", num1, " ", num2, file=out_file)
        print(max_capacity, file=out_file)
    
    ### Outputs
    if total_weight <= max_capacity:
        raise ValueError("Non-triviality condition on total weight violated")
    return


## QUBO reformulation of the KP
def kp_qubo(item_profits, item_weights, max_capacity, penalty_cte=1.0):
    
    """
    Defining the QUBO formulation of a KP instance
    ===============================================
    
    **Arguments**

        item_profits : 1D Numpy array
            The value of the profits
            associated with each item
            to be packed.
        item_weights : 1D Numpy array
            The value of the weights
            associated with each item
            to be packed.
        max_capacity : positive int
            The positive integer limiting
            the capacity of the knapsack.
        penalty_cte : float
            The QUBO penalty constant.

    **Outputs**
    
        qubo_matrix : 2D Numpy array
            The QUBO matrix defining the
            unconstrained KP objective function.
    
    **Details**

        Optimization variables are arranged along
        a one-dimensional chain, each site a binary
        variable. First, the binaries indicating whether
        an object is packed or not ({x_j}_{j=1}^n),
        followed by auxiliary variables to ensure the
        capacity constraint is met ({b_{l}_{l=0}^M}),
        where M is the bit-length of the maximum capacity
        value.
    """
    
    ### Reading input arguments
    c_bitlength = floor(log2(max_capacity))
    n_items = item_profits.size
    n_slack = c_bitlength + 1
    n_binaries = n_items + n_slack
    slack_prefactor = max_capacity + 1 - 2**c_bitlength
    qubo_matrix = zeros(shape=(n_binaries, n_binaries))
    
    ### QUBO matrix: diagonal elements
    for jj in range(n_items):
        qubo_matrix[jj][jj] = penalty_cte * item_weights[jj]**2
        qubo_matrix[jj][jj] -= item_profits[jj]
    for ll in range(n_slack - 1):
        qubo_matrix[n_items + ll][n_items + ll] = penalty_cte * 4**ll
    qubo_matrix[-1][-1] = penalty_cte * pow(slack_prefactor, 2)
    
    ### QUBO matrix: off-diagonal elements
    #### item-item interactions
    for jj in range(n_items - 1):
        for jj_prime in range(jj + 1, n_items):
            qubo_matrix[jj][jj_prime] = item_weights[jj] * item_weights[jj_prime]
            qubo_matrix[jj][jj_prime] *= 2 * penalty_cte
    #### slack-slack interactions
    for ll in range(n_slack - 2):
        for ll_prime in range(ll + 1, n_slack - 1):
            qubo_matrix[n_items + ll, n_items + ll_prime] = 2**(ll + ll_prime)
            qubo_matrix[n_items + ll, n_items + ll_prime] *= 2 * penalty_cte
    for ll in range(n_slack - 1):
        qubo_matrix[n_items + ll][n_binaries - 1] = 2**(ll + 1) * penalty_cte
        qubo_matrix[n_items + ll][n_binaries - 1] *= slack_prefactor
    #### item-slack interactions
    for  jj in range(n_items):    
        for ll in range(n_slack - 1):
            qubo_matrix[jj][n_items + ll] = 2**ll * item_weights[jj]
            qubo_matrix[jj][n_items + ll] *= -2 * penalty_cte
        qubo_matrix[jj][n_binaries - 1] = 2 * penalty_cte * item_weights[jj]
        qubo_matrix[jj][n_binaries - 1] *= -slack_prefactor
         
    ### Output
    return qubo_matrix


## QUBO to spinglass Ising KP
## Method 1
def qubo_to_ising_couplings(qubo_matrix):
    
    """
    Mapping the QUBO matrix onto spinglass couplings
    =================================================
    
    **Arguments**
    
        qubo_matrix : 2D Numpy array
            The QUBO matrix characterizing a
            KP instance.
    
    **Outputs**

        couplings_dict : dict
            The set of couplings defining the
            spinglass Hamiltonian encoding the
            KP instance solution.
            Specifically
                - 'offset': the constant term proportional
                            to the identity operator.
                            This constant term will be added
                            later once the spectrum has been
                            found and it's necessary to reconstruct
                            the cost of the solution to the original
                            combinatorial optimization problem;
                - 'one-qubit': the set of single-body couplings,
                               i.e., the set of longitudinal magnetic
                               fields, one for each qubit in the system;
                - 'two-qubit': the set of two-body (in general all-to-all)
                               couplings describing the interactions
                               between pairs of qubits.
    """
    
    ### Initializing function variables
    n_sites = qubo_matrix.shape[0]
    qubo_diagonal = diagonal(qubo_matrix).copy()
    two_body_interactions = triu(qubo_matrix, k=1)
    
    ### Energy offset
    cte = 0.5 * npsum(qubo_diagonal) + 0.25 * npsum(two_body_interactions)
    
    ### Single-binary couplings, aka, spinglass magnetic fields
    full_qubo_off_diag = two_body_interactions + two_body_interactions.T
    magnetic_fields = 0.5 * qubo_diagonal
    for jj in range(n_sites):
        for jj_prime in range(n_sites):
            if jj_prime != jj:
                magnetic_fields[jj] += 0.25 * full_qubo_off_diag[jj][jj_prime]
    #magnetic_fields = 0.5 * qubo_diagonal + 0.25 * npsum(two_body_interactions, axis=1)
    
    ### Output
    couplings_dict = {
        'offset': cte,
        'one-qubit': magnetic_fields,
        'two-qubit': two_body_interactions * 0.25
        }
    return couplings_dict

## Method 2
## NOTE: do not look at this function
## Still under debugging
def spinglass_model(item_profits, item_weights, max_capacity, penalty_cte=1.0):
    
    """
    Implementing the spinglass model of a KP instance
    ==================================================
    
    Starting from a KP instance, the function computes
    the couplings defining the corresponding spinglass
    model, obtained by mapping the problem to QUBO and
    then binary variables to spin variables.
    Here, the couplings are implemented directly, without
    going through the QUBO matrix. This function should
    obtain the same couplings as the previous one.
    
    **Arguments**

        item_profits : 1D Numpy array
            The value of the profits
            associated with each item
            to be packed.
        item_weights : 1D Numpy array
            The value of the weights
            associated with each item
            to be packed.
        max_capacity : positive int
            The positive integer limiting
            the capacity of the knapsack.
        penalty_cte : float
            The QUBO penalty constant.

    **Outputs**
    
        couplings_dict : dict
            The set of couplings defining the
            spinglass Hamiltonian encoding the
            KP instance solution.
            Specifically
                - 'offset': the constant term proportional
                            to the identity operator.
                            This constant term will be added
                            later once the spectrum has been
                            found and it's necessary to reconstruct
                            the cost of the solution to the original
                            combinatorial optimization problem;
                - 'one-qubit': the set of single-body couplings,
                               i.e., the set of longitudinal magnetic
                               fields, one for each qubit in the system;
                - 'two-qubit': the set of two-body (in general all-to-all)
                               couplings describing the interactions
                               between pairs of qubits.
    
    **Details**

        Optimization variables are arranged along
        a one-dimensional chain, each site a binary
        variable. First, the binaries indicating whether
        an object is packed or not ({x_j}_{j=1}^n),
        followed by auxiliary variables to ensure the
        capacity constraint is met ({b_{l}_{l=0}^M}),
        where M is the bit-length of the maximum capacity
        value.
    """
    
    ### Reading input arguments
    c_bitlength = floor(log2(max_capacity))
    n_items = item_profits.size
    n_slack = c_bitlength + 1
    n_binaries = n_items + n_slack
    total_available_weight = npsum(item_weights)
    slack_prefactor = max_capacity + 1 - 2**c_bitlength
    
    ### Initializing variables
    cte = 0
    psum = 0
    magnetic_fields = zeros(n_binaries)
    two_body_interactions = zeros(shape=(n_binaries, n_binaries))
    
    ### Computing the constant factor
    for pj, wj in zip(item_profits, item_weights):
        cte += penalty_cte * wj * wj - pj
    cte *= 0.5
    for jj in range(n_items - 1):
        for jj_prime in range(jj + 1, n_items):
            psum += item_weights[jj] * item_weights[jj_prime]
    for ll in range(n_slack - 2):
        for ll_prime in range(ll + 1, n_slack - 1):
            psum += 2**(ll + ll_prime)
    psum += slack_prefactor * (slack_prefactor - total_available_weight)
    psum += 2**n_slack - 1 + (2**c_bitlength - 1) * total_available_weight
    cte += 0.5 * penalty_cte * psum
    
    ### Computing single-qubit couplings, aka magnetic fields
    #### Item magnetic fields
    for jj, (pj, wj) in enumerate(zip(item_profits, item_weights)):
        magnetic_fields[jj] += 0.5 * (
            penalty_cte * wj * (wj - max_capacity) - pj
            )
    for jj in range(n_items - 1):
        magnetic_fields[jj] += penalty_cte * item_weights[jj] * npsum([
            item_weights[jj_prime]
            for jj_prime in range(jj + 1, n_items)
            ])
    #### Slack magnetic fields
    for ll in range(n_slack - 1):
        magnetic_fields[n_items + ll] += 0.5 * penalty_cte * 2**ll * (
            2 + 2**c_bitlength + total_available_weight + max_capacity
            )
    for ll in range(n_slack - 2):
        magnetic_fields[n_items + ll] += penalty_cte * 2**ll * npsum([
            2**ll_prime
            for ll_prime in range(ll + 1, n_slack - 1)
            ])
    magnetic_fields[-1] += 0.5 * penalty_cte * slack_prefactor * (
        max_capacity + 0.5 - 0.5 * 2**c_bitlength - total_available_weight
        )
    
    ### Computing two-qubit couplings, aka spin-spin interactions
    #### item-item interactions
    for jj in range(n_items - 1):
        for jj_prime in range(jj + 1, n_items):
            two_body_interactions[jj][jj_prime] += item_weights[jj] * item_weights[jj_prime]
    #### slack-slack interactions
    for ll in range(n_slack - 2):
        for ll_prime in range(ll + 1, n_slack - 1):
            two_body_interactions[n_items + ll, n_items + ll_prime] += 2**(ll + ll_prime)
    for ll in range(n_slack - 1):
        two_body_interactions[n_items + ll][-1] += slack_prefactor * 2**ll
    #### item-slack interactions
    for jj in range(n_items):
        for ll in range(n_slack - 1):
            two_body_interactions[jj][n_items + ll] -= 2**ll * item_weights[jj]
        two_body_interactions[jj][-1] -= slack_prefactor * item_weights[jj]
    two_body_interactions *= 0.5 * penalty_cte
    
    ### Output
    couplings_dict = {
        'offset': cte,
        'one-qubit': magnetic_fields,
        'two-qubit': two_body_interactions
        }
    return couplings_dict


## Helper functions
## Computation of the total profit cost function
def compute_total_profit(item_profits, optimized_bitstring):
    
    """
    Computing the value of the KP cost function
    ============================================
    
    **Arguments**
    
        item_profits : 1D Numpy array
            The value of the profits
            associated with each item
            to be packed.
        optimized_bitstring : 1D Numpy array
            The bit-string representing
            an item configuration optimized
            via some classical or quantum
            (-inspired) algorithm.
            The j-th 0/1 value corresponds
            to item j.
    
    **Outputs**
    
        total_profit : int
            The total profit of
            the knapsack associated
            to the input item configuration.
    """
    
    ### Checking input arguments
    if item_profits.size != optimized_bitstring.size:
        raise ValueError("The number of items must match the"
                         " number of instance profits parameters.")
    
    ### Output
    return int(npdot(item_profits, optimized_bitstring))

## Check-function for the capacity constraint
def check_max_capacity(item_weights, optimized_bitstring, max_capacity):
    
    """
    Checking the maximum capacity constraint
    =========================================
    
    **Arguments**
    
        item_weights : 1D Numpy array
            The value of the weights
            associated with each item
            to be packed.
        optimized_bitstring : 1D Numpy array
            The bit-string representing
            an item configuration optimized
            via some classical or quantum
            (-inspired) algorithm.
            The j-th 0/1 value corresponds
            to item j.
        max_capacity : positive int
            The positive integer limiting
            the capacity of the knapsack.
    
    **Outputs**

        flag : bool
            True if the input bistring satisfies
            the KP inequality constraint, False
            otherwise.
        total_weight : int
            The total weight of
            the knapsack associated
            to the input item configuration. 
    """
    
    ### Checking input arguments
    if item_weights.size != optimized_bitstring.size:
        raise ValueError("The number of items must match the"
                         " number of instance weights parameters.")
    
    ### Output
    total_weight = npdot(item_weights, optimized_bitstring)
    flag = True if total_weight <= max_capacity else False
    return flag, int(total_weight)