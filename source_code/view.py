import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent
import Barrier
import pprint
from model import Model 

# Initialize model
model = Model()

# Create initial plot
trace = go.Scatter(
    x=[agent.position[0] for agent in model.agents],
    y=[agent.position[1] for agent in model.agents],
    mode='markers',
    marker=dict(size=10)
)

# Create subplot
fig = make_subplots(
    rows=1,
    cols=1,
    subplot_titles=['Random Walk Animation!'],
    specs=[[{'type': 'scatter'}]]
)
fig.add_trace(trace)


for barrier in model.barriers:
    fig.add_shape(type="rect",
                    x0=barrier.A[0],
                    y0=barrier.A[1],
                    x1=barrier.B[0],
                    y1=barrier.B[1],
                    line=dict(color="Black"))


# Update layout
fig.update_layout(
    title='Random Walk Animation',
    xaxis=dict(range=[-20, 20]),
    yaxis=dict(range=[-20, 20]),
)



# Frames for animation
frames = []

# DATA VARIABLES
tot_sus = []
tot_exp = []
tot_inf = []

# Perform random walk for a certain number of steps
for step in range(model.num_steps):
    num_sus, num_exp, num_inf = model.step()

    frame = go.Frame(data=[
        go.Scatter(
            x=[agent.position[0] for agent in model.agents],
            y=[agent.position[1] for agent in model.agents],
            mode='markers')],
        name=f'Frame {step + 1}')

    frames.append(frame)

    # DATA TRACKING
    tot_sus.append(num_sus)
    tot_exp.append(num_exp)
    tot_inf.append(num_inf)


fig.frames = frames

# Update layout for animation
fig.update_layout(updatemenus=[
    dict(type='buttons',
         showactive=False,
         buttons=[dict(label='Play',
                       method='animate', args=[None, dict(
                           frame=dict(duration=200, redraw=True),
                           fromcurrent=True)])])])

# Show animation
fig.show()


# DATA GRAPHING 
# TODO: I know it's ugly, please bear with the hard code until I can parameterize

x_timestep = [i for i in range(1, model.num_steps)] 

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







