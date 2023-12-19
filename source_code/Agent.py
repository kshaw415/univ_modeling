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
        self.cur_time = 0
        self.exposure_time = []

    def __str__(self): 
        return f"{self.id} infected_status: {self.infected}"
    
    def random_walk(self, barrier=None): 
        '''
        update: check if barrier collision happens before calculating new angle 
        find behavior that ALWAYS redirects agent that next proposed coordinate is not on 
        otherside of the behavior 
        '''
        angle = np.random.uniform(0, 2 * np.pi)
        step_size = 1; # STEP SIZE, CHANGE IF DESIRED 
        new_x = self.position[0] + step_size * np.cos(angle)
        new_y = self.position[1] + step_size * np.sin(angle)

        # check for barrier collision 
        if barrier and barrier.is_collision(self):
            # Reflect the direction of movement upon collision
            angle = np.arctan2(self.position[1] - barrier.y, self.position[0] - barrier.x) + np.pi
            new_x = self.position[0] + step_size * np.cos(angle)
            new_y = self.position[1] + step_size * np.sin(angle)

        self.position = [new_x, new_y] # update Agent location 
        return self.position
    
    def agent_distance(self, agent2, cur_time, threshold): 
        '''
        Calculates Euclidean distance from another agent using distance formula
        
        '''
        # TO DO: directionality difference? 
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
            self.cur_time = cur_time # update time 

        return distance
    
    def get_exposed(self): 
        '''
        Determines if current agent is exposed based on close contacts 

        returns self with updated self.infected and self.exposure_time status 
        '''
        # if agent itself is already infected or 
        if self.infected == 2:
            return self  
        else: 
            # Susceptible 
            infected_contacts = 0 # counter
            for contact in self.contacts[self.cur_time]: 
                if contact.infected == 2: 
                    infected_contacts += 1

            if infected_contacts > 0:
                self.infected == 1
                self.exposure_time.append(self.cur_time)
            
        return self 
    
    def det_transmission(self): 
        '''
        Determines if an agent that is exposed becomes infected. 
        Updates Agent's infected status

        Output: Boolean
            True --> if agent is currently infected
            False --> if agent is not infected (can still be exposed) 
        '''
        # agent is already infected - returns True for infected 
        if self.infected == 2: 
            return True 
        
        # no exposure 
        elif self.infected == 0: 
            return False 
    
        else: 
            random_num = np.random.rand()
            p_transmit = 0.3 # CAN CHANGE - perhaps make threshold value, user input
            if random_num < p_transmit: # transmission occurs 
                self.infected = 2 
        
        return True if self.infected == 2 else False 



