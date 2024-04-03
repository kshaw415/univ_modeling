import random 
import simulator
import numpy as np
import multiprocessing

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


def run(seed, barrier_file, param_file): 
    output = simulator(seed, "barrier.csv", "params.csv") 
    return output 


if __name__ == "__main__": 
    num_processes = 4 # number of processes to parallelize
    seeds = generate_seeds(num_processes)

    # parallelized 
    with multiprocessing.Pool() as pool: 
        results = pool.map(run, seeds)

    # not parallelized (old)
    for i, seed in enumerate(seeds): 
        np.random.seed(seed)

        barrier_file = "barrier.csv"
        params_file = "params.csv"

        simulator(seed, barrier_file, params_file)

    
    """
    write a loop for each scenario 
    run function should include for loop set up 
        this seed, this barrier, this param row, then run 

    do a loop of 10 on local machine, then try oscar 

    do some timing/bench marking so we can figure out how long 
        do interactive session first (if takes longer than 15 min) call seiji and 
            do sbatch 
        write file to call handler with specific arguments for seed objects, barriers, params
            have sbatch header to say this is # cores needed, cpus, etc. 
            need 28 cpus, submit from command line 
    """
