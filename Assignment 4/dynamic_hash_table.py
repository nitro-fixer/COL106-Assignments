from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table_size = self.table_size
        self.table_size = get_next_size()
        
        if self.collision_type == "Chain":
            old_arr = self.array
            self.array = [[] for i in range(self.table_size)]
            for i, bucket in enumerate(old_arr):
                if bucket:
                    for key in bucket:
                        self.insert(key)
                    
        if self.collision_type in ["Linear", "Double"]:
            old_arr = self.array
            self.array = [None for i in range(self.table_size)]
            for i, key in enumerate(old_arr):
                if key is not None:
                    self.insert(key)
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # IMPLEMENT THIS FUNCTION
        old_table_size = self.table_size
        self.table_size = get_next_size()
        
        if self.collision_type == "Chain":
            old_arr = self.array
            self.array = [[] for i in range(self.table_size)]
            for i, bucket in enumerate(old_arr):
                if bucket:
                    for key in bucket:
                        self.insert(key)
                    
        if self.collision_type in ["Linear", "Double"]:
            old_arr = self.array
            self.array = [None for i in range(self.table_size)]
            for i, key in enumerate(old_arr):
                if key is not None:
                    self.insert(key)
        
    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()