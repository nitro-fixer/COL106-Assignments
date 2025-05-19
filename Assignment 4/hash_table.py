from prime_generator import get_next_size

def p(s):
    if s == 'a':
        return 0
    if s == 'A':
        return 26
    if s in 'bcdefghijklmnopqrstuvwxyz':
        return p('a') + (ord(s) - ord('a'))
    if s in 'BCDEFGHIJKLMNOPQRSTUVWXYZ':
        return p('A') + (ord(s) - ord('A'))

def h1(c, z, s):
    sum = 0
    for i in range(len(s)):
        sum += p(s[i]) * (z ** i)
    sum = sum % c
    return sum

def h2(c, z, s):
    sum = 0
    for i in range(len(s)):
        sum += (p(s[i]) * (z ** i))
    sum = c - (sum % c)
    return sum

def tuple_to_str(t):
    s = "(" + t[0] + ", " + str(t[1]) + ")"
    return s

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''
        self.collision_type = collision_type
        
        if self.collision_type == "Chain":
            self.z = params[0]
            self.initial_table_size = params[1]
            
        elif self.collision_type == "Linear":
            self.z = params[0]
            self.initial_table_size = params[1]
            
        elif self.collision_type == "Double":
            self.z1 = params[0]
            self.z2 = params[1]
            self.c2 = params[2]
            self.initial_table_size = params[3]
            
        self.table_size = self.initial_table_size
        self.array = ([None for i in range(self.table_size)] if self.collision_type in ["Linear", "Double"] else [[] for i in range(self.table_size)])
        self.elements = 0
    
    def insert(self, x):
        pass
    
    def find(self, key):
        pass
    
    def get_slot(self, key):
        pass
    
    def get_load(self):
        return (self.elements / self.table_size)
    
    def __str__(self):
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
    
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, key):
        if self.collision_type == "Chain":
            hash1 = h1(self.table_size, self.z, key)
            for i in self.array[hash1]:
                if i == key: break
            else:
                self.array[hash1].append(key)
                self.elements += 1
            
        if self.collision_type == "Linear":
            hash1 = h1(self.table_size, self.z, key)
            while self.array[hash1] is not None:
                if self.array[hash1] == key:
                    break
                hash1 = (hash1 + 1) % self.table_size
            else:
                self.array[hash1] = key
                self.elements += 1
        
        if self.collision_type == "Double":
            hash1 = h1(self.table_size, self.z1, key)
            hash2 = h2(self.c2, self.z2, key)
            while self.array[hash1] is not None:
                if self.array[hash1] == key:
                    break
                hash1 = (hash1 + hash2) % self.table_size
            else:
                self.array[hash1] = key
                self.elements += 1
    
    def find(self, key):
        if self.collision_type == "Chain":
            hash1 = h1(self.table_size, self.z, key)
            if key in self.array[hash1]:
                return True
            return False
        
        if self.collision_type == "Linear":
            hash1 = h1(self.table_size, self.z, key)
            while self.array[hash1] is not None:
                if self.array[hash1] == key:
                    return True
                hash1 = (hash1 + 1) % self.table_size
            return False
        
        if self.collision_type == "Double":
            hash1 = h1(self.table_size, self.z1, key)
            hash2 = h2(self.c2, self.z2, key)
            while self.array[hash1] is not None:
                if self.array[hash1] == key:
                    return True
                hash1 = (hash1 + hash2) % self.table_size
            return False
    
    def get_slot(self, key):
        if self.collision_type == "Chain":
            hash1 = h1(self.table_size, self.z, key)
            return hash1
        
        if self.collision_type == "Linear":
            hash1 = h1(self.table_size, self.z, key)
            while self.array[hash1] is not None:
                if self.array[hash1] == key:
                    return hash1
                hash1 = (hash1 + 1) % self.table_size
            return None
        
        if self.collision_type == "Double":
            hash1 = h1(self.table_size, self.z1, key)
            hash2 = h2(self.c2, self.z2, key)
            while self.array[hash1] is not None:
                if self.array[hash1] == key:
                    return hash1
                hash1 = (hash1 + hash2) % self.table_size
            return None
    
    def get_load(self):
        return (self.elements / self.table_size)
    
    def __str__(self):
        s = ""
        
        if self.collision_type == "Chain":
            for i in self.array:
                if i == []:
                    s += "<EMPTY>"
                else:
                    for j in i:
                        s += j
                        s += " ; "
                    s = s.rstrip(" ;")
                    
                s += " | "
                
            s = s.rstrip(" |")
            return s
        
        if self.collision_type in ["Linear", "Double"]:
            for i in self.array:
                if i is None:
                    s += "<EMPTY>"
                
                else:
                    s += str(i)
                
                s += " | "
            s = s.rstrip(" |")
            return s
    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x):
        # x = (key, value)
        if self.collision_type == "Chain":
            hash1 = h1(self.table_size, self.z, x[0])
            for i in range(len(self.array[hash1])):
                if self.array[hash1][i][0] == x[0]:
                    self.array[hash1][i] = x
                    break
            else:
                self.array[hash1].append(x)
                self.elements += 1
            
        if self.collision_type == "Linear":
            hash1 = h1(self.table_size, self.z, x[0])
            while self.array[hash1] is not None:
                if self.array[hash1] == x[0]:
                    self.array[hash1] = x
                    break
                hash1 = (hash1 + 1) % self.table_size
            else:
                self.array[hash1] = x
                self.elements += 1
        
        if self.collision_type == "Double":
            hash1 = h1(self.table_size, self.z1, x[0])
            hash2 = h2(self.c2, self.z2, x[0])
            while self.array[hash1] is not None:
                if self.array[hash1] == x[0]:
                    self.array[hash1] = x
                    break
                hash1 = (hash1 + hash2) % self.table_size
            else:
                self.array[hash1] = x
                self.elements += 1
    
    def find(self, key):
        if self.collision_type == "Chain":
            hash1 = h1(self.table_size, self.z, key)
            for i in range(len(self.array[hash1])):
                if self.array[hash1][i][0] == key:
                    return self.array[hash1][i][1]
            else:
                return None
        
        if self.collision_type == "Linear":
            hash1 = h1(self.table_size, self.z, key)
            while self.array[hash1] is not None:
                if self.array[hash1][0] == key:
                    return self.array[hash1][1]
                hash1 = (hash1 + 1) % self.table_size
            return None
                
        if self.collision_type == "Double":
            hash1 = h1(self.table_size, self.z1, key)
            hash2 = h2(self.c2, self.z2, key)
            while self.array[hash1] is not None:
                if self.array[hash1][0] == key:
                    return self.array[hash1][1]
                hash1 = (hash1 + hash2) % self.table_size
            return None
    
    def get_slot(self, key):
        if self.collision_type == "Chain":
            hash1 = h1(self.table_size, self.z, key)
            return hash1
        
        if self.collision_type == "Linear":
            hash1 = h1(self.table_size, self.z, key)
            while self.array[hash1] is not None:
                if self.array[hash1][0] == key:
                    return hash1
                hash1 = (hash1 + 1) % self.table_size
            return None
                
        if self.collision_type == "Double":
            hash1 = h1(self.table_size, self.z1, key)
            hash2 = h2(self.c2, self.z2, key)
            while self.array[hash1] is not None:
                if self.array[hash1][0] == key:
                    return hash1
                hash1 = (hash1 + hash2) % self.table_size
            return None
        
    def get_load(self):
        return (self.elements / self.table_size)
    
    def __str__(self):
        s = ""
        
        if self.collision_type == "Chain":
            for i in self.array:
                if i == []:
                    s += "<EMPTY>"
                
                else:
                    for j in i:
                        s += tuple_to_str(j) 
                        s += " ; "
                s = s.rstrip(" ;")
                s += " | "
            s = s.rstrip(" |")
            return s
        
        if self.collision_type in ["Linear", "Double"]:
            for i in self.array:
                if i is None:
                    s += "<EMPTY>"
                
                else:
                    s += tuple_to_str(i)
                
                s += " | "
            s = s.rstrip(" |")
            return s
