import numpy as np 
import random 
from random import seed
from random import randint
import math 
from collections import defaultdict
from pprint import pprint 
from Barrier import Barrier

# HELPER FUNCTIONS
# helper for agent_distance - credit: geeksforgeeks
# https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def onSegment(p, q, r): 
    '''
    Given 3 collinear points (self, agent2, r) the function checks if agent2
    lies on line segment self and r 
    inputs: 
    p, q, r
    r --> barrier.A or barrier.B, list of x&y coordinates
    [ function not written by Kiku]
    '''
    p_x = p[0]
    p_y = p[1]
    q_x = q[0]
    q_y = q[1]
    r_x = r[0]
    r_y = r[1]

    if ( (q_x <= max(p_x, r_x)) and (q_x >= min(p_x, r_x)) and \
        (q_y <= max(p_y, r_y)) and (q_y >= min(p_y, r_y))): 
        return True
    
    return False 

def orientation(p, q, r): 
    """
    find orientation of an ordered triplet. 

    output: 
    0: collinear points
    1: clockwise points
    2: counterclockwise 

    [ function not written by Kiku, see reference link above ]
    """
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0): # clockwise
        return 1 
    
    elif (val < 0): 
        return 2 # ccw
    
    else: 
        return 0 #collinear 
    
def doIntersect(p1, q1, p2, q2): 
    """
    returns true if p1, q1 (agent segment) and p2q2 (barrier) intersect

    [ function not written by Kiku, see reference link above ]
    """
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1) 
    o4 = orientation(p2, q2, q1) 

    # general case
    if ((o1 != o2) and (o3 != o4)): 
        return True
    
    # special cases
    # p1, q1 and p2 are collinear and p2 lies on segmetn p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)): 
        return True
    # p1, q1 and q2 are collinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)): 
        return True
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o3 == 0) and onSegment(p2, p1, q2)): 
        return True
    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2 
    if ((o4 == 0) and onSegment(p2, q1, q2)): 
        return True
    
    # if none of the cases
    return False 
    

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
        self.position = [x, y]
        self.cur_time = 0
        self.exposure_time = []
        self.infected_time = 0
        self.symptom_time = 0 

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
    

    def agent_distance(self, agent2, cur_time, threshold, barriers): 
        '''
        Calculates Euclidean distance from another agent using distance formula
        
        update: need to also consider barrier locations 
        '''
        
        distance = math.dist(self.position, agent2.position)
        # determine if we identify as a contact 
        if distance <= threshold: 
            # determine if barrier in between them (thus, no actual contact)
            for barrier in barriers: 
                p1 = self.position
                q1 = agent2.position
                p2 = barrier.A
                q2 = barrier.B
                if doIntersect(p1, q1, p2, q2): 
                    break 
            # No barriers intersect - can update contact dict     
            if cur_time in self.contacts: 
                self.contacts[cur_time].append([agent2, distance]) 
                agent2.contacts[cur_time].append([self, distance]) 
            else: 
                self.contacts[cur_time] = [[agent2, distance]]
                agent2.contacts[cur_time] = [[self, distance]]
            self.cur_time = cur_time # update time 

        return self
    
    def get_exposed(self): 
        '''
        Determines if agent is exposed based on close contacts 

        returns self with updated self.infected and self.exposure_time status 

        # TODO: implement a pmf to see if they infect another person 
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
    
    def get_infected(self): 
        '''        
        Determines if an agent that is exposed becomes infected. 
        Updates Agent's infected status

        Output: Boolean
            True --> if agent is currently infected
            False --> if agent is not infected (exposed OR susceptible) 
        '''
        # agent is already infected - returns True for infected 
        if self.infected == 2: 
            self.infected_time += 1 
            return True 
        
        # no exposure 
        elif self.infected == 0: 
            return False 
        
        elif len(self.exposure_time) > 0: 
            if self.exposure_time[-1] > 200: # after 200 time steps, no longer exposed. 
                self.exposure_time = []
                self.infected == 0
    
        else: 
            random_num = np.random.rand() # uniform draw U(0, 1) 
            p_transmit = 0.01 # CAN CHANGE - perhaps make threshold value, user input
            if random_num < p_transmit: # transmission occurs 
                self.infected = 2 
                self.infected_time += 1
        
        return True if self.infected == 2 else False 

    def get_symptoms(self): 
        """
        Determines if an agent that is infected becomes symptomatic 
        
        import numpy as np

        # Define the mean parameter
        mu = 3

        # Generate random numbers following the Poisson distribution
        random_numbers = np.random.poisson(mu, size=10)


        # Parameters of the Poisson distribution
        mu = 3

        # Number of events to calculate the PMF for
        k_values = np.arange(0, 10)  # For example, calculate PMF for events from 0 to 9

        # Calculate the PMF
        pmf_values = np.poisson.pmf(k_values, mu)
        """
        return True


    def recover(self): 
        """
        Recover based on time infected 
        
        """
        if self.symptom_time == 7:  # CAN CHANGE, after 7 time steps they are infected
            self.infected = 0 
