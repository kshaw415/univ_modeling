import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import Agent
import Barrier
import pprint

class Model: 
    """
    Model class to run the model
    """

    def __init__(self): 
        """
        Initialization method for the ABM
        
        Fields: 
            params --> csv file with necessary params (not yet iplemented)
        
        # TODO: implement actual params file, the following initialization is 
            HARDCODED
        """
        self.num_agents = 25
        self.distance_threshold = 2
        self.num_steps = 200
        self.agents = []
        self.agent_positions = []
        self.barriers = []

        for i in range(self.num_agents): 
            agent_id = i
            infected_status = np.random.choice([0, 1, 2]) # CAN CHANGE FOR MORE WEIGHTED/do we want to start with ANY exposed people? 
            agent = Agent.Agent(agent_id, infected_status)
            self.agents.append(agent)
            self.agent_positions.append(agent.position)

        barrier_0 = Barrier.Barrier([0,0], [0,10])
        barrier_1 = Barrier.Barrier([0,0], [10,0])
        barrier_2 = Barrier.Barrier([7, 10], [10, 10])
        barrier_3 = Barrier.Barrier([10, 10], [10, 0])
        self.barriers.append(barrier_0)
        self.barriers.append(barrier_1)
        self.barriers.append(barrier_2)
        self.barriers.append(barrier_3)

    def step(self): 
        """
        Perform a setp of the model 
        """
        num_sus = 0 
        num_exp = 0 
        num_inf = 0 

        for i, agent in enumerate(self.agents): 
            self.agent_positions[i] = agent.random_walk(self.barriers)

            # update agent status
            agent.agent_distance(self.agents[i], i, self.distance_threshold) # [i + 1]?
            agent.get_exposed()
            agent.get_infected()

            if agent.infected == 0: 
                num_sus += 1
            elif agent.infected == 1: 
                num_exp += 1
            elif agent.infected == 2: 
                num_inf += 1
        
        print(num_sus)
        return num_sus, num_exp, num_inf 
    