import numpy as np 
import random 
import math 
from collections import defaultdict

class Agent: 
    '''
    class for individual agents. 

    Fields: 
        
    
    '''

    def __init__(self, id: int, infected: int): 
        '''
        Initialization method for Agent class

        Fields: 
            id --> int, unique agent ID
            infected --> int, 0 if Susceptible, 1 if exposed, 2 if infected
            contacts --> dict, contains all contacts. key is time step, value 
                                is list of Agent 
        '''
        self.id = id
        self.infected = infected
        self.contacts = defaultdict(list)
        self.position = np.random.rand(1, 2) # x, y location 
        self.position = self.position.tolist()[0]

    def __str__(self): 
        return f"{self.id} infected_status: {self.infected}"
    
    def random_walk(self): 
        angle = np.random.uniform(0, 2 * np.pi)
        step_size = 1; # STEP SIZE, CHANGE IF DESIRED 
        new_x = self.position[0] + step_size * np.cos(angle)
        new_y = self.position[1] + step_size * np.sin(angle)
        self.position = [new_x, new_y] # update Agent location 
        return self.position
    
    def agent_distance(self, agent2, cur_time, threshold): 
        '''
        Calculates Euclidean distance from another agent using distance formula
        
        '''
        # TO DO: directionality difference? 
        # if distance already calculated, do not execute
        # if agent2 in self.contacts[cur_time]: 
        #     return self.contacts[] # MAYBE CHANGE??
        distance = math.dist(self.position, agent2.position)
        # determine if we identify as a contact 
        if distance <= threshold: 
            # update contact dict
            if cur_time in self.contacts: 
                self.contacts[cur_time].append([agent2, distance]) # MIGHT BECOME A SPACE ISSUE
                agent2.contacts[cur_time].append([self, distance]) # MIGHT BECOME A SPACE ISSUE 
            else: 
                self.contacts[cur_time] = [[agent2, distance]]
                agent2.contacts[cur_time] = [[self, distance]]

        return distance



    
    