import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent
import Barrier
import pprint

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

    # barrier = Barrier.Barrier(x=-10.0, y=0.0, width=0.1, height=10) # can adjust 
    # barrier2 = Barrier.Barrier(x=10.0,y=0.0, width=0.1, height=10)
    # barrier3 = Barrier.Barrier(x=0, y=10, width=10, height=0.1)
    # barrier4 = Barrier.Barrier(x=0, y=-10, width=10, height=0)

    barrier_new = Barrier.Barrier(A=[0,0], B=[0,2])
       
        # create initial plot 
    trace = go.Scatter(
        x = [agent.position[0] for agent in agents], 
        y = [agent.position[1] for agent in agents], 
        mode='markers', marker=dict(size=10)
    )

    barriernew_trace = go.Scatter(
        x = [barrier_new.A[0], barrier_new.B[0]],
        y = [barrier_new.A[1], barrier_new.B[1]],
        mode='lines', 
        line=dict(color='black', width=1), 
        fill='toself', 
        name='Barrier New'
    )
###
    # # barrier trace 
    # barrier_trace = go.Scatter(
    #     x=[barrier.x, barrier.x + barrier.width, barrier.x + barrier.width, barrier.x, barrier.x],
    #     y=[barrier.y, barrier.y, barrier.y + barrier.height, barrier.y + barrier.height, barrier.y],
    #     mode='lines',
    #     line=dict(color='red', width=2),
    #     fill='toself',
    #     name='Barrier'
    # )

    # barrier_trace2 = go.Scatter(
    #     x=[barrier2.x, barrier2.x + barrier2.width, barrier2.x + barrier2.width, barrier2.x, barrier2.x],
    #     y=[barrier2.y, barrier2.y, barrier2.y + barrier2.height, barrier2.y + barrier2.height, barrier2.y],
    #     mode='lines',
    #     line=dict(color='blue', width=2),
    #     fill='toself',
    #     name='Barrier2'
    # )

    # barrier_trace3 = go.Scatter(
    #     x=[barrier3.x, barrier3.x + barrier3.width, barrier3.x + barrier3.width, barrier3.x, barrier3.x],
    #     y=[barrier3.y, barrier3.y, barrier3.y + barrier3.height, barrier3.y + barrier3.height, barrier3.y],
    #     mode='lines',
    #     line=dict(color='green', width=2),
    #     fill='toself',
    #     name='Barrier3'
    # )

    # barrier_trace4 = go.Scatter(
    #     x=[barrier4.x, barrier4.x + barrier4.width, barrier4.x + barrier4.width, barrier4.x, barrier4.x],
    #     y=[barrier4.y, barrier4.y, barrier4.y + barrier4.height, barrier4.y + barrier4.height, barrier4.y],
    #     mode='lines',
    #     line=dict(color='purple', width=2),
    #     fill='toself',
    #     name='Barrier4'
    # )
###
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
    fig.add_trace(barriernew_trace)
    # fig.add_trace(barrier_trace)
    # fig.add_trace(barrier_trace2)
    # fig.add_trace(barrier_trace3)
    # fig.add_trace(barrier_trace4)

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
            agent_positions[i] = agent.random_walk(barrier_new) # this is def sus 
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
    