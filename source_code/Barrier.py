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

        # TO DO: fix. 
        """
        if (agent.position[0] < self.x + self.width and 
            agent.position[1] < self.y + self.height and 
            agent.position[1] > self.y): 
            return True
        return False 
    




    
