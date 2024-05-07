import numpy as np
from qtealeaves.modeling import QuantumModel
from qtealeaves.modeling import RandomizedLocalTerm, TwoBodyAllToAllTerm1D

# local disorder sampler
def loc_rand(params):
    # seeding
    qtrand = np.random.RandomState()
    if "seed" not in params:
        print("Attention: Running with default seed")
    # seed the random numbers
    qtrand.seed(params.get("seed", [11, 13, 17, 19]))
    # skip 1000 numbers
    _ = qtrand.random(1000)
    # get normal disorder
    vec = qtrand.normal(0,1,params['L'])
    return vec

# two-body disorder sampler
def twobody_rand(params):
    # seeding
    qtrand = np.random.RandomState()
    if "seed" not in params:
        print("Attention: Running with default seed")
    # seed the random numbers
    qtrand.seed(params.get("seed", [11, 13, 17, 19]))
    # skip 1000+L numbers 
    L = params['L']
    _ = qtrand.random(1000+L)
    # initialise disorder matrix
    coupling_matrix = np.zeros((L,L))
    # coupling pairs (with periodic boundaries)
    pairs = [(np.mod(i,L),np.mod(i+1,L)) for i in range(L)]
    # get ranomd numbers
    for (i,j) in pairs:
        coupling = np.random.normal(0,1)
        coupling_matrix[i,j] = coupling
        coupling_matrix[j,i] = coupling
    return coupling_matrix

# add disorder to model
def get_model(has_obc=False):
    
    # name model
    model_name = lambda params: "model with disorder"

    # select model type
    model = QuantumModel(1, "L", name=model_name)

    # local disorder
    model += RandomizedLocalTerm("ns", 
                                 # call the loc_rand function
                                 coupling_entries = loc_rand,
                                 strength = "disEs", 
                                 prefactor=+1)
    
    # two-body disorder
    model += TwoBodyAllToAllTerm1D(["sd","sa"], 
                                   # cal the twobody_rand function
                                   coupling_matrix=twobody_rand, 
                                   strength="disJt", 
                                   prefactor=+1)
    
    return model