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

def write_to_csv(timesteps, num_s, num_i): 
    """
    Names and writes output data to a unique csv file 
    Inputs: 
        timesteps --> list, time steps
        num_s --> list, number of susceptible agents at each time step
        num_i --> list, number of infected agents at each time step 
        #TODO: num_a --> list, number of active agents at each time step 
    """
    data = zip(timesteps, num_s, num_i)

    file_name = "testfilename.csv" #TODO: unique, using seed. 

    with open(file_name, mode='w', newline='') as file: 
        writer = csv.writer(file) 
        writer.writerow(['Time (in Seconds)', 'Susceptible Agents', 'Infected Agents'])
        writer.writerows(data)


if __name__ == "__main__": 
    
    ## Receive all data from params file ## 
    
    ## params for or referenced in simulation
    PARAM_num_agents = 0
    PARAM_distance_threshold = 0
    PARAM_symptom_threshold = 0
    PARAM_num_steps = 0
    PARAM_b0 = 0
    PARAM_b1 = 0
    PARAM_b2 = 0
    PARAM_b3 = 0
    PARAM_b4 = 0
    PARAM_immunity = False 
    
    ## params for Agent class only 
    # boundaries for simulation space 
    PARAM_xmin = 0
    PARAM_xmax = 0
    PARAM_ymin = 0 
    PARAM_ymax = 0 
    PARAM_masked = False 

    ## Initiate variables 
    num_agents = 50
    agents = []
    agent_positions = []
    THRESHOLD = 6
    symptom_THRESHOLD = 0.6 # TODO: this is COMPLETELY arbitrary 

    # Initialize agents with random positions
    for i in range(num_agents): 
        agent_id = i
        infected_status = np.random.choice([0, 2]) # CAN CHANGE FOR MORE WEIGHTED/do we want to start with ANY exposed people? 
        agent = Agent.Agent(agent_id, infected_status)
        agents.append(agent)
        agent_positions.append(agent.position)

    barriers = params.barrier_data("params - RoomsOpen.csv")
    

    # data for graphing/analysis 
    tot_sus = []
    tot_inf = []

    # Perform random walk for a certain number of steps
    num_steps = 1000 #28800 is 1 day (8 hours) 
    for step in range(num_steps):
        num_sus = 0
        num_exp = 0 
        num_inf = 0 

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
                agent = agent.agent_distance(agents, step, THRESHOLD, barriers) 

                if i == len(agents) - 1: 
                    break 
                else: 
                # Determine if an agent becomes infected 
                    if agent.get_infected(-4.95, 0, 0, 0, .03): 
                        # increase infected time
                        agent.infected_time += 1
                        
                        # determine if the agent gets symptoms
                        if agent.get_symptoms(symptom_THRESHOLD): 
                            agent.symptom_time += 1
                            agent.isolating = agent.self_isolate()

                        # determine if agent has recovered 
                        elif agent.symptom_time >= 200: # symptoms 
                            agent.recover(False) # TODO: param_immuity input
                    
            # output data
            if agent.infected == 0: 
                num_sus += 1
            elif agent.infected == 2: 
                num_inf += 1
            else: 
                print("curious this should never happen")

        tot_sus.append(num_sus)
        tot_inf.append(num_inf)


    # Output Data to CSV File 
    x_timestep = [i for i in range(1, num_steps)] 
    write_to_csv(x_timestep, tot_sus, tot_inf)