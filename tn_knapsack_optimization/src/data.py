"""Load the data"""

# %% 
import numpy as np 
from typing import List, Literal 
import os 

def read(file : str):
    # Loading an instance from the KP instances folder
    profits = []
    weights = []
    with open(file, 'r') as f:
        n_items = int(f.readline())
        for jj in range(n_items):
            _, pj, wj = f.readline().split()
            profits.append(pj)
            weights.append(wj)
        max_capacity = int(f.readline())
    profits = np.array(profits, dtype=int)
    weights = np.array(weights, dtype=int)

    return max_capacity, profits, weights

def load(dataset : Literal['small', 'medium', 'large'] = 'small', path : str = '../kp_instances'): 
    full_path = f'{path}/{dataset}'
    files = os.listdir(full_path)

    # Check on files, if they begin with kp we are almost 
    # sure they are the correct files
    files = [f'{full_path}/{file}' for file in files if file[:2] == 'kp']
    
    set : list = []
    for file in files:
        C, profits, weights = read(file)
        set.append({})
        set[-1]['C'] = C
        set[-1]['weights'] = list(weights)
        set[-1]['profits'] = list(profits)
        
    return set
