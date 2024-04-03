import random 
import simulator
import numpy as np


barrier_file = "Barriers.csv"
params_file = "Params.csv"

# run simulator.py 
def generate_seeds(n): 
    """
    Generates n number of seeds using the MRG32k3a algorithm
    """
    seeds = []

    # initialize prng
    prng = np.random.default_rng()

    for _ in range(n): 
        seed = prng.integers(0, np.iinfo(np.int32).max, dtype=np.int32)
        seeds.append(seed)

    return seeds 



if __name__ == "__main__": 
    num_processes = 4 # number of processes to parallelize
    seeds = generate_seeds(num_processes)

    for i, seed in enumerate(seeds): 
        np.random.seed(seed)

        # run model code here
        