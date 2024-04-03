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

### HELPER FUNCTIONS ###

def write_to_csv(timesteps, num_s, num_i, num_iso): 
    """
    Names and writes output data to a unique csv file 
    Inputs: 
        timesteps --> list, time steps
        num_s --> list, number of susceptible agents at each time step
        num_i --> list, number of infected agents at each time step 
        #TODO: num_a --> list, number of active agents at each time step 
    """
    data = zip(timesteps, num_s, num_i, num_iso)

    file_name = "testfilename.csv" #TODO: unique, using seed. 

    with open(file_name, mode='w', newline='') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Time (in Seconds)', 'Susceptible Agents', 'Infected Agents', 'Isolating Agents'])
        writer.writerows(data)


if __name__ == "__main__": 
    
    ## Receive all data from params file ## 
    xbounds, ybounds, distance_thresh, symptom_thresh, masking, \
        b0, b1, b2, b3, b4, num_agents, num_steps, immunity = params.parse_data("DataParams - Sheet1.csv")
    
    ## params for or referenced in simulation
    PARAM_num_agents = num_agents
    PARAM_distance_threshold = distance_thresh
    PARAM_symptom_threshold = symptom_thresh
    PARAM_num_steps = num_steps
    PARAM_b0 = b0
    PARAM_b1 = b1
    PARAM_b2 = b2
    PARAM_b3 = b3
    PARAM_b4 = b4
    PARAM_immunity = immunity 
    
    ## params for Agent class only 
    # boundaries for simulation space 
    PARAM_xboundaries = xbounds
    PARAM_yboundaries = ybounds

    PARAM_masking = False # True if masking is turned on 


    ## Initiate variables 
    agents = []
    agent_positions = []

    # PARAM_num_agents = 50 
    # THRESHOLD = 6
    # symptom_THRESHOLD = 0.6 # TODO: this is COMPLETELY arbitrary 

    # Initialize agents with random positions
    for i in range(PARAM_num_agents): 
        agent_id = i
        infected_status = np.random.choice([0, 1]) 
        agent = Agent.Agent(agent_id, infected_status, PARAM_masking, PARAM_xboundaries, PARAM_yboundaries)
        agents.append(agent)
        agent_positions.append(agent.position)

    barriers = params.barrier_data("params - RoomsOpen.csv")
    

    # data for graphing/analysis 
    tot_sus = []
    tot_inf = []
    tot_iso = []

    # Perform random walk for a certain number of steps
    # num_steps = 1000 #28800 is 1 day (8 hours) 
    for step in range(PARAM_num_steps):
        num_sus = 0
        num_inf = 0 
        num_iso = 0 

        for i in range(len(agents)):
            # identify current agent working on 
            agent = agents[i]
            
            if agent.isolating: 
                agent.infected_time += 1
                agent.symptom_time += 1
                if agent.symptom_time >= 200: 
                    agent.recover(False) #TODO: param_immunity input
            else: 
                # Take random step forward 
                agent.random_walk(barriers)
                agent = agent.agent_distance(agents, step, PARAM_distance_threshold, barriers) 

                if i == len(agents) - 1: 
                    break 
                else: 
                # Determine if an agent becomes infected 
                    if agent.get_infected(-4.95, 0, 0, 0, .03): 
                        # increase infected time
                        agent.infected_time += 1
                        
                        # determine if the agent gets symptoms
                        if agent.get_symptoms(PARAM_symptom_threshold): 
                            agent.symptom_time += 1
                            agent.isolating = agent.self_isolate()

                        # determine if agent has recovered 
                        elif agent.symptom_time >= 200: # symptoms 
                            agent.recover(False) # TODO: param_immuity input
                    
            # output data
            if agent.infected == 0: 
                num_sus += 1
            elif agent.infected == 1: 
                num_inf += 1
            else: 
                print("curious this should never happen")
            if agent.isolating: 
                num_iso += 1

        tot_sus.append(num_sus)
        tot_inf.append(num_inf)
        tot_iso.append(num_iso)


    # Output Data to CSV File 
    x_timestep = [i for i in range(1, PARAM_num_steps)] 
    write_to_csv(x_timestep, tot_sus, tot_inf, tot_iso) # TODO: number of people masked 