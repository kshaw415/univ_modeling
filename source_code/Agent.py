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

    def __init__(self, id: int, infected: int, PARAM_masking: bool, xboundaries : list, yboundaries : list): 
        '''
        Initialization method for Agent class

        Fields: 
            id --> int, unique agent ID
            infected --> int, 0 if Susceptible, 1 if infected
            contacts --> dict, contains all contacts. key is time step, value 
                                is list of Agent
            exposure_time --> list of times Agent has been exposed
        '''
        self.id = id
        self.infected = infected

        self.contacts = [] 
        self.contact_exposure = dict() # {contact.id, exposure_duration}
        
        x = randint(xboundaries[0], xboundaries[1]) 
        y = randint(yboundaries[0], yboundaries[1]) 
        self.position = [x, y]
        
        self.cur_time = 0
        self.exposure_time = []
        self.infected_time = 0
        self.can_symptoms = False # false if asymptomatic infection, True if eventually will become symptomatic 
        self.symptomatic = False # Symptom flagger, False if no symptoms, True if currently presenting symptoms
        self.symptom_time = 0 
        self.immune = False # True --> 
        
        # intervention
        if PARAM_masking: 
            num = random.uniform(0, 1)
            if num < 0.7: # 70% masking compliance 
                self.masked = True 
            else: 
                self.masked = False
        else: 
            self.masked = False
        self.isolating = False # True --> isolating and goes off screen until recover

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
    

    def agent_distance(self, agents, cur_time, threshold, barriers): 
        '''
        Calculates Euclidean distance from another agent using distance formula
        '''
        
        for agent2 in agents: 

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
                # No barriers intersect - can update contact if infected
                if agent2.infected == 1:  
                    self.contacts.append(agent2)    
                
                self.cur_time = cur_time # update time 


        return self
    
    
    def get_infected(self, PARAM_b0, PARAM_b1, PARAM_b2, PARAM_b3, PARAM_b4): 
        """
        Determines if an Agent that is exposed becomes infected. Update status 

        Input: 

        Output: 

        """
        def logodds(me_i, me_j, symp_status):    
            """
            Function that calculates the log odds based on the given parameters 
            
            Inputs: 
                me_i --> Boolean, Agent (denoted as i) masking status
                me_j --> Boolean, infected Agent (denoted as j) masking status 
                symp_status --> Boolean, symptomatic status of other Agent 

            Outputs: 

            """
            # TODO: can put beta for being symptomatic (more infectious sympt than asymp)
            result = PARAM_b0 + PARAM_b1*me_i + PARAM_b2*me_j + PARAM_b3*me_i*me_j + PARAM_b4*symp_status
            return result 
        
        def flag(status): 
            """
            returns 1 if True, 0 if False 
            """
            if status == True: 
                return 1 
            elif status == False: 
                return 0
            else: 
                print("Issue - not boolean") 

        # Scenario #1: already infected
        if self.infected == 1: 
            return True
        
        # Scenario #2: no exposures
        elif len(self.contacts) == 0: 
            return False 

        else: 
            for agent_j in self.contacts:
                # identify if masked
                me_j = flag(agent_j.masked)
                me_i = flag(self.masked)
                symp = flag(self.symptomatic)
                # calculate logodds 
                output = logodds(me_i, me_j, symp)
                p = 1 / (1 + math.exp(-output))
                
                # roll dice: determine if an infection event occurs (Bernoulli)
                infection_event = np.random.binomial(1, p, size=1) 

                if infection_event == 1: 
                    self.infected = 1 # update status 
                    # roll if they will become symptomatic 
                    p_sympt = 0.5 # TODO: Parameterize 
                    self.can_symptoms = np.random.binomial(1, p_sympt, size=1) # 1 --> going to become symptomatic. 
                    # define time when they will actually become symptomatic 
                    return True
            
        return False 
        
    def get_symptoms(self, symptom_onset_threshold): 
        """
        Determines if an agent that is infected becomes symptomatic. 
        # TODO: parameterize (user input) this value for symptom_threshold


        assign symptomatic flag once hit time of determined 
        check if currently >= symptom time threshold (if yes, become symptomatic) 

        """
        # infected, not symptomatic yet, but drew to be symptomatic 
        if self.infected == 1 and self.symptomatic == False and self.can_symptoms == True: 
            # Becomes symptomatic  
            if self.infected_time >= symptom_onset_threshold: 
                self.symptomatic = True 
                return True 
        else: 
            return False  


    def self_isolate(self): 
        """
        Self isolates based on symptom status
        """
        if self.symptomatic: 
            isolate_event = np.random.binomial(1, 0.7, size=1) # 70% isolates if symptomatic 
            if isolate_event == 1: 
                self.position = [-15, -13]
                return True 



    def recover(self, param_immunity): 
        """
        Recover based on time infected 
        # TODO: Update (3/28)
        """
        self.infected = 0 
        self.can_symptoms = False
        self.symptomatic = False 
        self.contacts = []
        self.contact_exposure = dict()
        self.exposure_time = []
        self.infected_time = 0
        self.isolating = False
        if param_immunity == True: 
            self.immune = True 
        else: 
            self.immune = False 
        return self 


