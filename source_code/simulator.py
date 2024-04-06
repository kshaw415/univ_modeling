import pytest
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent
import Barrier
import pprint
from model import Model 
import params
import multiprocessing
import random 
import csv 


def write_to_csv(seed, timesteps, num_s, num_i, num_iso, num_masked, simID): 
    """
    Names and writes output data to a unique csv file 
    Inputs: 
        timesteps --> list, time steps
        num_s --> list, number of susceptible agents at each time step
        num_i --> list, number of infected agents at each time step 
        num_iso --> list, number of active agents at each time step 
    """
    data = zip(timesteps, num_s, num_i, num_iso, num_masked)

    file_name = f'{simID}_{seed}_output.csv' 

    with open(file_name, mode='w', newline='') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Time (in Seconds)', 'Susceptible Agents', 'Infected Agents', 'Isolating Agents', 'Masked Agents'])
        writer.writerows(data)


def run_model(seed, barriers, parameters): 
    """
    Code to run a single simulation 
    """   
    random.seed(seed) # set the seed 

    ## Receive all data from params file ## 
    barriers = params.barrier_data("params - RoomsOpen.csv")

    # xbounds, ybounds, distance_thresh, symptom_thresh, masking, \
    #     b0, b1, b2, b3, b4, num_agents, num_steps, immunity = params.parse_data(param_file)

    ## params for or referenced in simulation
    PARAM_num_agents = parameters[12]
    PARAM_distance_threshold = parameters[4]
    PARAM_symptom_threshold = parameters[5]
    PARAM_num_steps = parameters[13]
    PARAM_p = parameters[7]
    PARAM_maski = parameters[8]
    PARAM_maskj = parameters[9]
    PARAM_maskij = parameters[10]
    PARAM_symptom_infect = parameters[11]
    PARAM_immunity = parameters[14] 
    PARAM_time_step = parameters[15]
    PARAM_recovery = parameters[16]
    ## params for Agent class only 
    # boundaries for simulation space 
    PARAM_xboundaries = [parameters[0], parameters[1]]
    PARAM_yboundaries = [parameters[2], parameters[3]]

    PARAM_masking = parameters[6] # True if masking is turned on 
    PARAM_sim_id = parameters[17]

    ## Initiate variables 
    agents = []
    agent_positions = []


    # Initialize agents with random positions
    for i in range(PARAM_num_agents): 
        agent_id = i
        infected_status = np.random.choice([0, 1]) 
        agent = Agent.Agent(agent_id, infected_status, PARAM_masking, PARAM_xboundaries, PARAM_yboundaries, PARAM_immunity)
        agents.append(agent)
        agent_positions.append(agent.position)



    # data for graphing/analysis 
    tot_sus = []
    tot_inf = []
    tot_iso = []
    tot_masked = []

    # Perform random walk for a certain number of steps
    # num_steps = 1000 #1 day is 960 at 30sec/time step --> 13440 for 2 weeks 
    for step in range(PARAM_num_steps):
        num_sus = 0
        num_inf = 0 
        num_iso = 0 
        num_masked = 0

        for i in range(len(agents)):
            # identify current agent working on 
            agent = agents[i]
            
            if agent.isolating: 
                agent.infected_time += 1
                agent.symptom_time += 1
                if agent.infected_time >= PARAM_recovery or agent.symptom_time >= PARAM_recovery: 
                    agent.recover(PARAM_immunity) 
            else: 
                # Take random step forward 
                agent.random_walk(barriers, PARAM_time_step)
                agent = agent.agent_distance(agents, step, PARAM_distance_threshold, barriers) 

                if i == len(agents) - 1: 
                    break 
                else: 
                # Determine if an agent becomes infected 
                    if agent.get_infected(PARAM_p, PARAM_maski, PARAM_maskj, PARAM_maskij, PARAM_symptom_infect): 
                        # increase infected time
                        agent.infected_time += 1
                        
                        # determine if the agent gets symptoms
                        if agent.get_symptoms(PARAM_symptom_threshold): 
                            agent.symptom_time += 1
                            agent.isolating = agent.self_isolate()

                        # determine if agent has recovered 
                        elif agent.infected_time >= PARAM_recovery or agent.symptom_time >= PARAM_recovery: # symptom recovery 3 days
                            agent.recover(PARAM_immunity) 
                    
            # output data
            if agent.infected == 0: 
                num_sus += 1
            elif agent.infected == 1: 
                num_inf += 1
            else: 
                print("curious this should never happen")
            if agent.isolating: 
                num_iso += 1
            if agent.masked == True: 
                num_masked += 1

        tot_sus.append(num_sus)
        tot_inf.append(num_inf)
        tot_iso.append(num_iso)
        tot_masked.append(num_masked)


    # Output Data to CSV File 
    x_timestep = [i for i in range(1, PARAM_num_steps)] 
    write_to_csv(seed, x_timestep, tot_sus, tot_inf, tot_iso, tot_masked, PARAM_sim_id) 