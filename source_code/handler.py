import random 
import simulator
import numpy as np
import multiprocessing
import pandas as pd
import time 

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



def run(row_seed_pair): 
    row, seed = row_seed_pair
    parameters = row 
    simulator.run_model(seed, "barrier.csv", parameters) 


if __name__ == "__main__": 
    start = time.time()
    
    seeds = generate_seeds(4) 

    params_df = pd.read_csv("DataParams - test2 (1).csv")
    params_seed_pairs = zip(params_df.values, seeds) 

    # parallelized 
    with multiprocessing.Pool(5) as pool: 
        pool.map(run, params_seed_pairs)

        
    end = time.time()
    print(end - start)
    print(multiprocessing.cpu_count())
    

