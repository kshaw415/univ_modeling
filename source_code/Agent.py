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
        self.contact_exposure = dict() # {contact.id, exposure_duration}
        x = randint(-14,14) # CAN CHANGE # TODO: Parameter
        y = randint(-12,12) # CAN CHANGE # TODO: Parameter
        self.position = [x, y]
        self.cur_time = 0
        self.exposure_time = []
        self.infected_time = 0
        self.can_symptoms = False # false if asymptomatic infection, True if eventually will become symptomatic 
        self.symptomatic = False # Symptom flagger, False if no symptoms, True if currently presenting symptoms
        self.symptom_time = 0 
        self.immune = False # True --> 

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
                # No barriers intersect - can update contact dict     
                if cur_time in self.contacts: 
                    self.contacts[cur_time].append([agent2, distance]) 
                    agent2.contacts[cur_time].append([self, distance]) 
                
                else: 
                    self.contacts[cur_time] = [[agent2, distance]]
                    agent2.contacts[cur_time] = [[self, distance]]

                # if other agent is infected: updating the contact_exposure dict {"agent id": int(duration of exposure)}
                # not needed - just consider dice is rolled each second 
                if agent2.infected == 2: 
                    if agent2.id in self.contact_exposure: 
                        self.contact_exposure[agent2.id] += 1
                    else: 
                        self.contact_exposure[agent2.id] = 1
                
                self.cur_time = cur_time # update time 


        return self
    
    def get_exposed(self): 
        '''
        Determines if agent is exposed based on close contacts 

        returns self with updated self.infected and self.exposure_time status

        TODO: exposure doesn't require count. We just determine close contact 
            and then it's like ooh infect

        '''
        # if agent itself is already infected or 
        if self.infected == 2 or self.immune == True:
            return False  
                
        else: 
            # Susceptible or exposed 
            infected_contacts = 0 # counter

            # Scenario 1: No close contacts 
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

                # for id, exposure_time in self.contact_exposure.items(): 
                #     if exposure_time > 900: # 900
                #         self.infected = 1 # become exposed 
                #         return True
            
        return False  
    

    def get_infected(self, PARAM_b0, PARAM_b1, PARAM_b2, PARAM_b3, PARAM_b4): 
        """
        Determines if an Agent that is exposed becomes infected. Update status 

        Input: 

        Output: 

        for each Agent they were exposed to...
            identify if other agent is masked
            assign me_j variable 
            calculate logodds with given inputs for beta values 

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


    def get_infected_old(self): 
        '''        
        Determines if an agent that is exposed becomes infected. 
        Updates Agent's infected status

        Output: Boolean
            True --> if agent is currently infected
            False --> if agent is not infected (exposed OR susceptible) 
        '''
        # IDENTIFYING INTERVENTION VARIABLES
        me_i = 0.045 #TODO: Parameterize
        me_j = 0.078 #TODO: Parameterize
        b0 = 1 #TODO: Identify
        b1 = 0 #TODO: Parameterize - 0 is base case 
        b2 = 0 #TODO: Parameterize
        b3 = 0 #TODO: Parameterize 
        b4 = 1 #TODO: Identify (symptomatic based adjustment) 
        # TODO: j agent symptom status

        def logodds(me_i, me_j, b0, b1, b2, b3, b4, t):    
            # TODO: can put beta for being symptomatic (more infectious sympt than asymp)
            return b0 + b1*me_i + b2*me_j + b3*me_i*me_j + b4*t

        # Scenario 1: Already Infected 
        if self.infected == 2: 
            return True 

        # Scenario 2: No exposures (no chance of becoming infected)
        elif self.infected == 1: 
            return False  
        
        # Scenario 3: Exposed to 1+ contacts 
        else: 
            for contact_id, exposure_duration in self.contact_exposure.items(): # for each infected contact... 
                # determine how long they've been exposed for 
                t = exposure_duration # TODO: symptom status of j 

                output = logodds(me_i, me_j, b0, b1, b2, b3, b4, t) 

                p = 1 / (1 + math.exp(-output)) 
                infection_event = np.random.binomial(1, p, size=1) 
                if infection_event == 1: 
                    self.infected = 2
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
        if self.infected == 2 and self.symptomatic == False and self.can_symptoms == True: 
            # Becomes symptomatic  
            if self.infected_time >= symptom_onset_threshold: 
                self.symptomatic = True 
                return True 
        
        return False  


    def recover(self, param_immunity): 
        """
        Recover based on time infected 
        # TODO: Update (3/28)
        """
        self.infected = 0 
        self.can_symptoms = False
        self.symptomatic = False 
        self.contacts = defaultdict(list)
        self.contact_exposure = dict()
        self.exposure_time = []
        self.infected_time = 0
        if param_immunity == True: 
            self.immune = True 
        else: 
            self.immune = False 
        return self 


