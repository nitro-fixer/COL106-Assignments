'''
    This file contains the class definition for the StrawHat class.
'''
from custom import comp_1, comp_2
from crewmate import CrewMate
from heap import Heap

class StrawHatTreasury:
    '''
    Class to implement the StrawHat Crew Treasury
    '''
    
    def __init__(self, m):
        '''
        Arguments:
            m : int : Number of Crew Mates (positive integer)
        Returns:
            None
        Description:
            Initializes the StrawHat
        Time Complexity:
            O(m)
        '''
        
        # Write your code here
        self.m = m
        self.crewmates_heap = Heap(comp_1, [])
        for i in range(self.m):
            self.crewmates_heap.insert(CrewMate())
    
    def add_treasure(self, treasure):
        '''
        Arguments:
            treasure : Treasure : The treasure to be added to the treasury
        Returns:
            None
        Description:
            Adds the treasure to the treasury
        Time Complexity:
            O(log(m) + log(n)) where
                m : Number of Crew Mates
                n : Number of Treasures
        '''
        
        # Write your code here
        crewm = self.crewmates_heap.extract()
        crewm.add_treasure(treasure)
        self.crewmates_heap.insert(crewm)

    def get_completion_time(self):
        """
        Arguments:
            None
        Returns:
            List[Treasure]: List of treasures sorted by their ids after processing
        Description:
            Processes all the treasures for each crewmate and returns them sorted by their ids after updating their completion times.
        Time Complexity:
            O(n(log(m) + log(n))) where:
                m: Number of Crew Mates
                n: Number of Treasures
        """
        
        
        processed_treasures = []
        
        for crewmate in self.crewmates_heap.array:
            if not crewmate.treasures:
                continue
            
            treasure_queue = Heap(comp_2, [])
            crewmate.update_treasures()
            current_index = 0
            
            while current_index < len(crewmate.treasures):
                current_treasure = crewmate.treasures[current_index]
                arrival_time = current_treasure.arrival_time
                
                treasure_queue.insert((current_treasure.get_priority(), current_treasure))
                next_arrival = (
                    crewmate.treasures[current_index + 1].arrival_time
                    if current_index + 1 < len(crewmate.treasures) else float('inf')
                )
                
                while arrival_time < next_arrival:
                    if treasure_queue.is_empty():
                        break
                    
                    top_treasure = treasure_queue.extract()[1]
                    
                    if top_treasure.rsize <= next_arrival - arrival_time:
                        arrival_time += top_treasure.rsize
                        top_treasure.completion_time = arrival_time
                        processed_treasures.append(top_treasure)
                    else:
                        top_treasure.rsize -= (next_arrival - arrival_time)
                        treasure_queue.insert((top_treasure.get_priority(), top_treasure))
                        arrival_time = next_arrival
                
                current_index += 1
                
            while not treasure_queue.is_empty():
                remaining_treasure = treasure_queue.extract()[1]
                arrival_time += remaining_treasure.rsize
                remaining_treasure.completion_time = arrival_time
                processed_treasures.append(remaining_treasure)
    
        processed_treasures.sort(key=lambda treasure: treasure.id)
        return processed_treasures
