import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent
import Barrier
import pprint

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


if __name__ == "__main__": 
    # Number of agents
    num_agents = 10
    agents = []
    agent_positions = []
    THRESHOLD = 6

    # Initialize agents with random positions
    for i in range(num_agents): 
        agent_id = i
        infected_status = np.random.choice([0, 1, 2]) # CAN CHANGE FOR MORE WEIGHTED
        agent = Agent.Agent(agent_id, infected_status)
        agents.append(agent)
        agent_positions.append(agent.position)

    barrier = Barrier.Barrier(x=0.0, y=0.0, width=0.1, height=10) # can adjust 
        # create initial plot 
    trace = go.Scatter(
        x = [agent.position[0] for agent in agents], 
        y = [agent.position[1] for agent in agents], 
        mode='markers', marker=dict(size=10)
    )

    # barrier trace 
    barrier_trace = go.Scatter(
        x=[barrier.x, barrier.x + barrier.width, barrier.x + barrier.width, barrier.x, barrier.x],
        y=[barrier.y, barrier.y, barrier.y + barrier.height, barrier.y + barrier.height, barrier.y],
        mode='lines',
        line=dict(color='red', width=2),
        fill='toself',
        name='Barrier'
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
    fig.add_trace(barrier_trace)

    fig.update_layout(
        xaxis=dict(range=[-20, 20]),  # Adjust the range as needed
        yaxis=dict(range=[-20, 20])   # Adjust the range as needed
        )
    
    # Frames for animation
    frames = []

    dist_list = []
    # Perform random walk for a certain number of steps
    num_steps = 100
    for step in range(num_steps):
        for i in range(num_agents):
            # update position 
            agent = agents[i]
            agent_positions[i] = agent.random_walk(barrier=barrier) # this is def sus 
            if i == num_agents - 1: # last agent, this is also awk
                break 
            else: 
                dist = agent.agent_distance(agents[i + 1], step, THRESHOLD) 
                dist_list.append(dist)
            
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
    
    # pprint.pprint(agents[i].contacts)
    fig.show()

    