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

### HELPER FUNCTIONS ###

def worker_function(seed):
    random.seed(seed) # Set
    result = random.random()
    return result 

# if __name__ == "__main__": 
#     num_processes = 4 # number of processes to parallelize
#     seeds = [123, 456, 789, 101112]
#     with multiprocessing.Pool(num_processes) as pool: 
#         results = pool.map(worker_function, seeds)
    
#     print("Results:", results) 



if __name__ == "__main__": 
    
    ## Receive all data from params file ## 
    PARAM_num_agents = 0
    PARAM_distance_threshold = 0
    PARAM_symptom_threshold = 0
    PARAM_num_steps = 0
    PARAM_b0 = 0
    PARAM_b1 = 0
    PARAM_b2 = 0
    PARAM_b3 = 0
    PARAM_b4 = 0
    

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

    # create initial plot 
    trace = go.Scatter(
        x = [agent.position[0] for agent in agents], 
        y = [agent.position[1] for agent in agents], 
        mode='markers', marker=dict(size=10)
    )

    # layout 
    layout = go.Layout(
        title='Random Walk Animation', 
        xaxis=dict(range=[0,1]), 
        yaxis=dict(range=[0,1]),)
    
    # create subplot 
    fig = make_subplots(
        rows=1, 
        cols=1, 
        subplot_titles=['Random Walk Animation!'], 
                        specs=[[{'type': 'scatter'}]])
    fig.add_trace(trace)
    # fig.add_trace(barriernew_trace)

    # Initial plot setup
    for barrier in barriers:
        fig.add_shape(type="rect",
                      x0=barrier.A[0],
                      y0=barrier.A[1],
                      x1=barrier.B[0],
                      y1=barrier.B[1],
                      line=dict(color="Black"))


    fig.update_layout(
        xaxis=dict(range=[-20, 20]),  # Adjust the range as needed
        yaxis=dict(range=[-20, 20])   # Adjust the range as needed
        )
    
    # Frames for animation
    frames = []

    # data for graphing/analysis 
    tot_sus = []
    tot_exp = []
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
            elif agent.infected == 1: 
                num_exp += 1 
            elif agent.infected == 2: 
                num_inf += 1
            else: 
                print("curious this should never happen")

        tot_sus.append(num_sus)
        tot_exp.append(num_exp)
        tot_inf.append(num_inf)

        # Create a frame for the current step
        frame = go.Frame(data=[
            go.Scatter(
                x = [agent.position[0] for agent in agents], 
                y = [agent.position[1] for agent in agents], 
                mode='markers')],
                name=f'Frame {step + 1}') 
        
        frames.append(frame)

    fig.frames = frames    

    # update layout for animation
    fig.update_layout(updatemenus=[
        dict(type='buttons', 
             showactive=False, 
             buttons=[dict(label='Play', 
                           method='animate', args=[None, dict(
                               frame=dict(duration=200, redraw=True), 
                               fromcurrent=True)])])])

    fig.show()


# graphing data
x_timestep = [i for i in range(1, num_steps)] 

traceSus = go.Scatter(
    x=x_timestep, 
    y=tot_sus, 
    mode='lines+markers', 
    name='Number of Susceptible Agents per Time Step'
)

layoutSus = go.Layout(
    title='Number of Susceptible Agents over Time', 
    xaxis=dict(title='Time Steps'), 
    yaxis=dict(title='Number of Susceptible Agents')
)

traceExp = go.Scatter(
    x=x_timestep, 
    y=tot_exp, 
    mode='lines+markers', 
    name='Number of Exposed Agents per Time Step'
)

traceInf = go.Scatter(
    x=x_timestep,
    y=tot_inf,
    mode='lines+markers',
    name='Number of Infected Agents per Time Step'
)

layoutExp = go.Layout(
    title='Number of Exposed Agents over Time', 
    xaxis=dict(title='Time Steps'), 
    yaxis=dict(title='Number of Exposed Agents')
)

layoutInf = go.Layout(
    title='Number of Infected Agents over Time', 
    xaxis=dict(title='Time Steps'), 
    yaxis=dict(title='Number of Infected Agents')
)

figSus = go.Figure(data=[traceSus], layout=layoutSus)
figExp = go.Figure(data=[traceExp], layout=layoutExp)
figInf = go.Figure(data=[traceInf], layout=layoutInf)

figSus.update_layout(yaxis_range=[0, num_agents])
figExp.update_layout(yaxis_range=[0, num_agents])
figInf.update_layout(yaxis_range=[0, num_agents])

figSus.show()
figExp.show()
figInf.show()
