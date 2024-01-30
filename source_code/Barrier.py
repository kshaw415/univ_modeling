import math 

class Barrier:
    '''
    class for Barriers that Agent class interacts with (think walls, etc.). 
    '''

    def __init__(self, A, B): 
        '''
        Barriers

        Fields: 
        A --> list of x&y coordinates 
        B --> list of x&y coordinates 

        # NOTE: make line vectors in __init__
        '''
        self.A = A
        self.B = B

    def mindistance(self, agent): 
        """
        Check if agent collides with barrier. Algorithm and code from 
        https://www.geeksforgeeks.org/minimum-distance-from-a-point-to-the-line-segment-using-vectors/

        Input: 
            agent --> Agent class object
        Output: 
            Boolean --> True if Agent is close enough to Barrier
        """
        THRESHOLD = 0.3 # arbitrary, should parametrize later

        # create Barrier vector 
        AB = [None, None] 
        AB[0] = self.B[0] - self.A[0]
        AB[1] = self.B[1] - self.A[1]

        # create Agent-A Vector (E is agent node)
        AE = [None, None] 
        AE[0] = agent.position[0] - self.A[0]
        AE[1] = agent.position[1] - self.A[1]

        # create Agent-A Vector (E is agent node)
        BE = [None, None] 
        BE[0] = agent.position[0] - self.B[0]
        BE[1] = agent.position[1] - self.B[1]

        # dot product 
        AB_BE = AB[0] * BE[0] + AB[1] * BE[1]
        AB_AE = AB[0] * AE[0] + AB[1] * AE[1]
        
        mindist = 0

        # Case 1: Agent (E) closest to B node 
        if AB_BE > 0: 
            y = agent.position[1] - self.B[1]
            x = agent.position[0] - self.B[0]
            mindist = math.sqrt(x * x + y * y)
        
        # Case 2: Agent (E) closest to A node
        elif AB_AE < 0: 
            y = agent.position[1] - self.A[1]
            x = agent.position[0] - self.B[0]
            mindist = math.sqrt(x * x + y * y)
    
        # Case 3: Agent (E) closest to perpendicular line of vector AB
        else: 
            # find perpendicular distance 
            x1 = AB[0] 
            y1 = AB[1] 
            x2 = AE[0] 
            y2 = AE[1]
            mod = math.sqrt(x1 * x1 + y1 * y1) 
            mindist = abs(x1 * y2 - y1 * x2) / mod 

        if mindist <= THRESHOLD:
            return True
        
        else:
            return False 
        
    def det_crossbarrier(self, cur_pos, next_pos): 
        '''
        Boolean function that determines if the step location crosses the barrier. 
        Inputs: 
            cur_pos --> list, [x,y] coordinates of Agent current position 
            next_pos --> list, [x,y] coordinates of Agent next proposed position 

        Output: 
            Boolean --> True if next_pos crosses Barrier, else False
        '''
        # Define vectors 
        v_barrier = (self.B[0] - self.A[0], self.B[1] - self.A[1])
        v_current = (cur_pos[0] - self.A[0], cur_pos[1] - self.A[1])
        v_step = (next_pos[0] - self.A[0], next_pos[1] - self.A[1])

        # Calculate cross products
        cp_current = v_barrier[0] * v_current[1] - v_barrier[1] * v_current[0]
        cp_next = v_barrier[0] * v_step[1] - v_barrier[1] * v_step[0]

        if (cp_current > 0) == (cp_next > 0): # on same side
            return False
        else: # proposed step crosses barrier
            return True






    
