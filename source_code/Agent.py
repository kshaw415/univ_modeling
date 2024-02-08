import numpy as np 
import random 
from random import seed
from random import randint
import math 
from collections import defaultdict
from pprint import pprint 
from Barrier import Barrier

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
            exposure_time --> list of times Agent has been exposed
        '''
        self.id = id
        self.infected = infected
        self.contacts = defaultdict(list) #dict([])
        x = randint(-10,10) # CAN CHANGE
        y = randint(-10,10) # CAN CHANGE
        # self.position = np.random.rand(1, 2) # x, y location 
        self.position = [x, y]
        # self.position = self.position.tolist()[0]
        self.cur_time = 0
        self.exposure_time = []

    def __str__(self): 
        return f"{self.id} infected_status: {self.infected}"
    
    def random_walk(self, barriers): 
        '''
        Random walk algorithm. 
        input: 
            barriers --> List<Barrier>
        output: 
            self.position --> new position coordinates for Agent
        '''
        step_size = 1; # STEP SIZE, CHANGE IF DESIRED 
        
        angle = np.random.uniform(0, 2 * np.pi)
        new_x = self.position[0] + step_size * np.cos(angle)
        new_y = self.position[1] + step_size * np.sin(angle)

        # determine out of bounds (not barrier within)
        if new_x > 15: 
            new_x -= 1
        if new_x < -15: 
            new_x += 1
        if new_y > 15: 
            new_y -= 1
        if new_y < -15: 
            new_y += 1

        # determine if new step crosses any barriers 
        # IF THIS DOESN'T WORK, remove the for loop. 
        for barrier in barriers: 
            cross_barrier = Barrier.det_crossbarrier(barrier, self.position, [new_x, new_y])
            while cross_barrier: 
                # choose new 
                angle = np.random.uniform(0, 2 * np.pi)
                new_x = self.position[0] + step_size * np.cos(angle)
                new_y = self.position[1] + step_size * np.sin(angle)
                cross_barrier = Barrier.det_crossbarrier(barrier, self.position, [new_x, new_y])
            
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
        Determines if agent is exposed based on close contacts 

        returns self with updated self.infected and self.exposure_time status 
        '''
        # if agent itself is already infected or 
        if self.infected == 2:
            return self  
        else: 
            # Susceptible or exposed 
            infected_contacts = 0 # counter
            if len(self.contacts) == 0: 
                return self
            else:
                close_contacts = self.contacts[self.cur_time]
                for contact in close_contacts: 
                    if contact[0].infected == 2: 
                        infected_contacts += 1

                if infected_contacts > 0:
                    self.infected = 1 # update status to exposed 
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
            random_num = np.random.rand() # uniform draw U(0, 1) 
            p_transmit = 0.03 # CAN CHANGE - perhaps make threshold value, user input
            if random_num < p_transmit: # transmission occurs 
                self.infected = 2 
        
        return True if self.infected == 2 else False 



