import matplotlib.pyplot as plt
import numpy as np

# Function to perform a random walk for an agent
def random_walk(position, step_size=1):
    # Generate random angles for movement
    angle = np.random.uniform(0, 2 * np.pi)
    
    # Calculate the new position based on the random angle
    new_x = position[0] + step_size * np.cos(angle)
    new_y = position[1] + step_size * np.sin(angle)
    
    return new_x, new_y

# Function to visualize the 2D space with agents
def visualize_space(agents):
    plt.figure(figsize=(8, 8))
    
    # Plot agents
    for agent in agents:
        plt.scatter(agent[0], agent[1], marker='o', color='blue')

    plt.title('2D Space with Random Walk Agents')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.show()

# Number of agents
num_agents = 10

# Initialize agents with random positions
agents = np.random.rand(num_agents, 2) * 10

# Perform random walk for a certain number of steps
num_steps = 100
for _ in range(num_steps):
    for i in range(num_agents):
        agents[i] = random_walk(agents[i])

# Visualize the 2D space with agents after random walk
visualize_space(agents)
