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

    barriers = []
    barrier_0 = Barrier.Barrier([0,0], [0,5])
    barrier_1 = Barrier.Barrier([0,0], [5,0])
    barriers.append(barrier_0)
    barriers.append(barrier_1)








    # create initial plot 
    trace = go.Scatter(
        x = [agent.position[0] for agent in agents], 
        y = [agent.position[1] for agent in agents], 
        mode='markers', marker=dict(size=10)
    )

    # barriernew_trace = go.Scatter(
    #     x = [barrier_0.A[0], barrier_0.B[0]],
    #     y = [barrier_0.A[1], barrier_0.B[1]],
    #     mode='lines', 
    #     line=dict(color='black', width=1), 
    #     fill='toself', 
    #     name='Barrier New'
    # )


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
    # Perform random walk for a certain number of steps
    num_steps = 100
    for step in range(num_steps):
        for i in range(num_agents):
            # update position 
            agent = agents[i]
            # need to go through barrier LIST (all barriers) 
            agent_positions[i] = agent.random_walk(barriers)
            if i == num_agents - 1: # last agent, this is also awk
                break 
            else: 
                # calling all methods 
                dist = agent.agent_distance(agents[i + 1], step, THRESHOLD) 
                dist_list.append(dist)
                agent.get_exposed()
                agent.det_transmission()

        # Create a frame for the current step
        frame = go.Frame(data=[
            go.Scatter(
                x = [agent.position[0] for agent in agents], 
                y = [agent.position[1] for agent in agents], 
                mode='markers')],
                # marker={'color': ['red' if agent.infected == 2 else 'yellow' if agent.infected == 1 else 'blue']})],
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
    
    for i in agents: 
        print(str(i))
    fig.show()
    