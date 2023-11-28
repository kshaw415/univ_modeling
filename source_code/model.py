import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent

# Function to perform a random walk for an agent
def random_walk(position, step_size=1):
    # Generate random angles for movement
    angle = np.random.uniform(0, 2 * np.pi)
    
    # Calculate the new position based on the random angle
    new_x = position[0] + step_size * np.cos(angle)
    new_y = position[1] + step_size * np.sin(angle)
    
    return new_x, new_y

if __name__ == "__main__": 
    test_agent = Agent.Agent(0, 0)
    print(test_agent.position)

    # Number of agents
    num_agents = 10

    # Initialize agents with random positions
    agents = np.random.rand(num_agents, 2) * 10

    # create initial plot 
    trace = go.Scatter(
        x = agents[:,0], y = agents[:, 1], mode='markers', marker=dict(size=10)
    )

    # layout 
    layout = go.Layout(
        title='Random Walk Animation', xaxis=dict(range=[0,1]), yaxis=dict(range=[0,1]),)
    
    # create subplot 
    fig = make_subplots(rows=1, cols=1, subplot_titles=['Random Walk Animation!'], 
                        specs=[[{'type': 'scatter'}]])
    fig.add_trace(trace)
    
    fig.update_layout(
        xaxis=dict(range=[-20, 20]),  # Adjust the range as needed
        yaxis=dict(range=[-20, 20])   # Adjust the range as needed
)


    # Frames for animation
    frames = []

    # Perform random walk for a certain number of steps
    num_steps = 100
    for step in range(num_steps):
        for i in range(num_agents):
            # update position 
            agents[i] = random_walk(agents[i])
        
        # Create a frame for the current step
        frame = go.Frame(data=[
            go.Scatter(x=agents[:, 0], 
                       y=agents[:, 1], 
                       mode='markers')],
            name=f'Frame {step+1}')
        
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

