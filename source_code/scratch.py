import numpy as np
def transmission_prob(I, I_N, N, T, S): 
    """
    Function to calcualte probability. Taken from Method 1 from 
    https://www.nature.com/articles/s41598-017-09209-x#ref-CR5

    B = disease transmission coefficient (transmission rate)
    a = recovery rate
    S = number of susceptible indviduals
    I = number of infected individuals
    N = total number of individuals 
    I_N = number of new infections since previous sampling 
    T = sampling interval (1 day = 1) 
    """
    B = -1*np.log(1 - I_N / I) / (T * S / N)
    
    P = 1 - np.exp(-(B * I) / N) # probability of infection for each susceptible individual 
    return P