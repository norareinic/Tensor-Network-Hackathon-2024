import numpy as np
import qtealeaves as qtl
from qtealeaves.operators import TNOperators
from qtealeaves.modeling import QuantumModel, LocalTerm, LindbladTerm

# embedding
def get_operators():
    
    # define exciton operators
    ops_e = TNOperators()

    # identity matrix
    ops_e.ops['id'] = np.eye(3)

    # singlet and triplet dagger
    ops_e.ops['sd'] = np.array([[0, 0, 0], [1., 0, 0], [0, 0, 0.]])
    ops_e.ops['td'] = np.array([[0, 0, 0], [0, 0, 0], [1., 0, 0.]])

    # singlet and triplet annihilation
    ops_e.ops['sa'] = np.transpose(ops_e.ops['sd'])
    ops_e.ops['ta'] = np.transpose(ops_e.ops['td'])

    # define phonon operators (bosons)
    # ---------------------------
    ops_b = qtl.operators.TNBosonicOperators()

    # combine exciton-phonon operators
    my_ops = qtl.operators.TNCombinedOperators(ops_e, ops_b)

    return my_ops

# adding composite operators to model
def get_model(has_obc=False):
   
    # name model
    model_name = lambda params: "exciton_phonon_model"

    # model 
    model = QuantumModel(1, "L", name=model_name)

    # local singlet energy (ns on exciton, id on phonon)
    model += LocalTerm("ns.id", strength="Es")

    # bosons (id on exciton, n on phonon)
    model += LocalTerm("id.n", strength="w0")

    # exciton-phonon interactions
    model += LocalTerm("ns.bdagger", strength="gs")
    model += LocalTerm("ns.b", strength="gs")

    # local Lindblad terms on bosons
    model += LindbladTerm("id.bdagger", strength="k_plus")
    model += LindbladTerm("id.b", strength="k_minus")

    return model