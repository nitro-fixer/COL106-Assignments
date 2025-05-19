'''
    Python file to implement the class CrewMate
'''

class CrewMate:
    '''
    Class to implement a crewmate
    '''
    
    def __init__(self):
        '''
        Arguments:
            None
        Returns:
            None
        Description:
            Initializes the crewmate
        '''
        
        # Write your code here
        self.load = 0
        self.treasures = []
    
    # Add more methods if required
    def add_treasure(self, treasure):
        self.treasures.append(treasure)
        self.load = max(self.load, treasure.arrival_time) + treasure.size
        self.treasures.sort(key=lambda x: x.arrival_time)
        
    def update_treasures(self):
        for treasure in self.treasures:
            treasure.initialise_rsize()