import math 

class Barrier:
    '''
    class for Barriers that Agent class interacts with (think walls, etc.). 
    '''

    def __init__(self, x, y, width, height):
        '''
        Barriers. Need to consider how to initialize a continuous space. 

        Fields: 
        x --> width of Space
        y --> length of Space
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_collision(self, agent): 
        """
        Check if agent collides with barrier 

        # TO DO: fix. DISTANCE ONLY DOING BASED ON INITIAL POSITIO - NOT INCLUDING 
        WIDTH OR HEIGHT!!! 
        """


        # this needs to re-implement to vector math + dot product shtuff
        distance = math.dist(agent.position, [self.x, self.y])

        if distance < 0.1: 
            return True
        else: 
            return False 

        # if (agent.position[0] < self.x + self.width and 
        #     agent.position[1] < self.y + self.height and 
        #     agent.position[1] > self.y): 
        #     return True
        # return False 
    




    
