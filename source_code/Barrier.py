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







    
