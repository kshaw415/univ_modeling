import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent
import Barrier
import pprint

if __name__ == "__main__": 
    # Number of agents
    num_agents = 50
    agents = []
    agent_positions = []
    THRESHOLD = 6

    # Initialize agents with random positions
    for i in range(num_agents): 
        agent_id = i
        infected_status = np.random.choice([0, 1, 2]) # CAN CHANGE FOR MORE WEIGHTED/do we want to start with ANY exposed people? 
        agent = Agent.Agent(agent_id, infected_status)
        agents.append(agent)
        agent_positions.append(agent.position)

    # barrier = Barrier.Barrier(x=-10.0, y=0.0, width=0.1, height=10) # can adjust 
    # barrier2 = Barrier.Barrier(x=10.0,y=0.0, width=0.1, height=10)
    # barrier3 = Barrier.Barrier(x=0, y=10, width=10, height=0.1)
    # barrier4 = Barrier.Barrier(x=0, y=-10, width=10, height=0)

    barriers = []
    barrier_0 = Barrier.Barrier([0,0], [0,10])
    barrier_1 = Barrier.Barrier([0,0], [10,0])
    barrier_2 = Barrier.Barrier([7, 10], [10, 10])
    barrier_3 = Barrier.Barrier([10, 10], [10, 0])
    barriers.append(barrier_0)
    barriers.append(barrier_1)
    barriers.append(barrier_2)
    barriers.append(barrier_3)


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
    num_steps = 1000
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
                dist = agent.agent_distance(agents[i + 1], step, THRESHOLD) 
                dist_list.append(dist)
                agent.get_exposed()
                agent.det_transmission()
            
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

    figSus.show()
    figExp.show()
    figInf.show()