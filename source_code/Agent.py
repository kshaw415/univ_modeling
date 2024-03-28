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
        x = randint(-14,14) # CAN CHANGE # TODO: Parameter
        y = randint(-12,12) # CAN CHANGE # TODO: Parameter
        self.position = [x, y]
        self.cur_time = 0
        self.exposure_time = []
        self.infected_time = 0
        self.symptom_time = 0 

        # intervention
        self.masking = False # TODO: Parameter
        

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
        if new_y > 13: 
            new_y -= 1
        if new_y < -13: 
            new_y += 1

        # determine if new step crosses any barriers 
        # IF THIS DOESN'T WORK, remove the for loop. 
        # TODO: allows for barrier crossing if passes first barrier, but then chooses new one. 
        for barrier in barriers: 
            cross_barrier = Barrier.det_crossbarrier(barrier, self.position, [new_x, new_y])
            while cross_barrier: 
                # choose new 
                angle = np.random.uniform(0, 2 * np.pi)
                new_x = self.position[0] + step_size * np.cos(angle)
                new_y = self.position[1] + step_size * np.sin(angle)
                cross_barrier = Barrier.det_crossbarrier(barrier, self.position, [new_x, new_y])
                        
        old = self.position
        self.position = [new_x, new_y] # update Agent location 
        # print(math.dist(old, self.position))

        return self.position
    

    def agent_distance(self, agent2, cur_time, threshold, barriers): 
        '''
        Calculates Euclidean distance from another agent using distance formula
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
            return False  
        else: 
            if self.masking: 
                # Masking 
                close_contacts = self.contacts[self.cur_time]
                for contact in close_contacts: 
                    # if contact was masked 
                    if contact.masking: 
                        # determine exposure based on time
                        pass
                    else: 
                        if contact[0].infected == 2: 
                            infected_contacts += 1
            
            else: 
                # Susceptible or exposed 
                infected_contacts = 0 # counter
                if len(self.contacts) == 0: 
                    return False
                else:
                    close_contacts = self.contacts[self.cur_time]
                    for contact in close_contacts: 
                        if contact[0].infected == 2: 
                            infected_contacts += 1

                    if infected_contacts > 0:
                        self.infected = 1 # update status to exposed 
                        self.exposure_time.append(self.cur_time)
            
        return True  
    
    def get_infected(self): 
        '''        
        Determines if an agent that is exposed becomes infected. 
        Updates Agent's infected status

        Output: Boolean
            True --> if agent is currently infected
            False --> if agent is not infected (exposed OR susceptible) 


            TODO: for loop for each infected contacts YUH
        '''
        # IDENTIFYING INTERVENTION VARIABLES
        me_i = 0.01 #TODO: Parameterize
        me_j = 0.01 #TODO: Parameterize
        b0 = 1 #TODO: Parameterize
        b1 = 1 #TODO: Parameterize
        b2 = 1 #TODO: Parameterize
        b3 = 1 #TODO: Parameterize 

        # Confirm this is what math works cuz the logit thing is not logiting for me 
        def logp(me_i, me_j): 
            return b0 + b1*me_i + b2*me_j + b3*me_i*me_j

        output = logp(me_i, me_j) 

        p = 1 / (1 + math.exp(-(b0 + b1 + b2 + b3))) # TODO: do exp on the negative of output) math.exp(-(output))
        p_transmit = np.random.binomial(1, p, size=1) 

        # agent is already infected - returns True for infected 
        if self.infected == 2: 
            # self.infected_time += 1 
            return True 
        
        # no exposure 
        elif self.infected == 0: 
            return False 
        
        elif len(self.exposure_time) > 0: 
            if self.exposure_time[-1] > 200: # after 200 time steps, no longer exposed. # TODO: use paramter
                self.exposure_time = []
                self.infected = 0 
    
        else: # TODO: --> Get rid of, no longer necessary 
            random_num = np.random.rand() # uniform draw U(0, 1) 
            p_transmit = 0.03 # CAN CHANGE - perhaps make threshold value, user input
            if random_num < p_transmit: # transmission occurs 
                self.infected = 2 
        
        return True if self.infected == 2 else False 

    def get_symptoms(self, symptom_threshold): 
        """
        Determines if an agent that is infected becomes symptomatic. 
        # TODO: parameterize (user input) this value 
        """
        # TODO: Simple binomial draw for person is symptomatic or asymptomatic 
            # X days after infection (lag --> parameter) 
        
        # Identify what day since exposure 
        exposure_prob = symptom_threshold # this will be a FUNCTION
        random_num = np.random.rand()
        if random_num < exposure_prob: 
            # self.symptom_time += 1 # start symptom counter 
        
            return True 
        return False 


    def recover(self): 
        """
        Recover based on time infected 
        
        """
        self.infected = 0 
        self.symptom_time = 0
        self.contacts = defaultdict(list)
        self.exposure_time = []
        self.infected_time = 0
        self.symptom_time = 0 
        return self 


'''
Funciton takes input on probability scale 
- the equations constrain always on level of probability (can't get p > 1)
- #TODO: come up with a vector of reasonable probabilities for the per second 
         
- don't take distance into account; model could be made more flexible 

file:///Users/kikuyoshaw/Downloads/COVID%2019%20topological%20influences.pdf
- 

B4 (distance) 
- set to 1 
- 

simulation: 
- how does chaging B1, 2 etc. affet infected
linear on log odds scale 
change in probability will follow sigmoid function 


find reasonable betas for B0, B4 
    - search different assumptions about B1, B2, B3

    

'''