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

### HELPER FUNCTIONS
def remove_from_pop(agent, agents): 
    """
    Agent is infected and symptomatic. They are removed from population and return after 5 days (14400 sec) 
    """
    
    return True



if __name__ == "__main__": 
    # Number of agents
    num_agents = 50
    agents = []
    agent_positions = []
    THRESHOLD = 6
    symptom_THRESHOLD = 0.6 # TODO: this is COMPLETELY arbitrary 

    # Initialize agents with random positions
    for i in range(num_agents): 
        agent_id = i
        infected_status = np.random.choice([0, 2]) # CAN CHANGE FOR MORE WEIGHTED/do we want to start with ANY exposed people? 
        # print(infected_status)
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

    dist_list = []

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

        for i in range(num_agents):
            # update position 
            agent = agents[i]
            # need to go through barrier LIST (all barriers) 
            agent_positions[i] = agent.random_walk(barriers)
            if i == num_agents - 1: # last agent, this is also awk
                break 
            else: 
                # calling all methods 
                dist = agent.agent_distance(agents[i + 1], step, THRESHOLD, barriers) 
                dist_list.append(dist)
                if agent.get_exposed(): # if agent gets exposed
                    if len(agent.exposure_time) > 86400: # if agent exposed for 3 days...
                        agent.recover() # be susceptible again
                if agent.get_infected(): # if agent is infected
                    agent.infected_time += 1
                    if agent.get_symptoms(symptom_THRESHOLD): 
                        agent.symptom_time += 1
                    if agent.symptom_time >= 1000: # symptoms 
                        agent.recover()
                
            
            # output data
            if agent.infected == 0: 
                num_sus += 1
            elif agent.infected == 1: 
                num_exp += 1 
            elif agent.infected == 2: 
                num_inf += 1
            else: 
                print("oh no they are immune")
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
    
    # for i in agents: 
        # print(str(i))

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

