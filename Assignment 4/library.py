import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, book_titles, texts):
        self.book_titles = book_titles
        self.temp_books = book_titles.copy()
        self.mergesort(self.temp_books)
        self.texts = texts
        for text in self.texts:
            self.mergesort(text)
        
        self.indices = [self.book_titles.index(book) for book in self.temp_books]
        self.unique = [self.distinct_words(book) for book in self.book_titles]
        
    
    def distinct_words(self, book_title):
        l = []
        tindex = self.binsearch(self.temp_books, book_title)
        index = self.indices[tindex]
        
        for i in self.texts[index]:
            if len(l) == 0:
                l.append(i)
            else:
                if i == l[-1]:
                    continue
                else:
                    l.append(i)
                    
        return l
    
    def count_distinct_words(self, book_title):
        index = self.binsearch(self.temp_books, book_title)
        return len(self.unique[self.indices[index]])
    
    def search_keyword(self, keyword):
        l = []
        for i in range(len(self.temp_books)):
            if self.binsearch(self.unique[self.indices[i]], keyword) != -1:
                l.append(self.temp_books[i])
        return l
    
    def print_books(self):
        for i in range(len(self.temp_books)):
            s = self.temp_books[i] + ": "
            
            for j in self.unique[self.indices[i]]:
                s += j + " | "
                
            s = s.rstrip(" |")
            print(s)
    
    def mergesort(self, s):
        n = len(s)
        if n < 2: return
        
        mid = n // 2
        s1 = s[0:mid]
        s2 = s[mid:n]
        
        self.mergesort(s1)
        self.mergesort(s2)
        
        self.merge(s1, s2, s)
    
    def merge(self, s1, s2, s):
        i = j = 0
        while i + j < len(s):
            if j == len(s2) or (i < len(s1) and s1[i] < s2[j]):
                s[i+j] = s1[i]
                i += 1
            else:
                s[i+j] = s2[j]
                j += 1
                
    def binsearch(self, l, target):
        left = 0
        right = len(l) - 1
        mid = 0
        
        while left <= right:
            mid = (left + right) // 2
            
            if l[mid] < target:
                left = mid + 1
                
            elif l[mid] > target:
                right = mid - 1
                
            else:
                return mid
        
        return -1

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        self.name = name
        self.params = params
        
        if self.name == "Jobs":
            self.hm = ht.HashMap("Chain", params)
        elif self.name == "Gates":
            self.hm = ht.HashMap("Linear", params)
        elif self.name == "Bezos":
            self.hm = ht.HashMap("Double", params)
    
    def add_book(self, book_title, text):
        if self.name == "Jobs":
            hs = ht.HashSet("Chain", self.params)
            for i in text:
                hs.insert(i)
                
        elif self.name == "Gates":
            hs = ht.HashSet("Linear", self.params)
            for i in text:
                hs.insert(i)
                
        elif self.name == "Bezos":
            hs = ht.HashSet("Double", self.params)
            for i in text:
                hs.insert(i)
        
        self.hm.insert((book_title, hs))
    
    def distinct_words(self, book_title):
        l = []
        hs = self.hm.find(book_title)
        if hs.collision_type in ["Linear", "Double"]:
            for i in hs.array:
                if i is not None:
                    l.append(i)
            return l
        
        elif hs.collision_type == "Chain":
            for i in hs.array:
                if i != []:
                    for j in i:
                        l.append(j)
            return l
    
    def count_distinct_words(self, book_title):
        hs = self.hm.find(book_title)
        return hs.elements
    
    def search_keyword(self, keyword):
        l = []
        if self.hm.collision_type in ["Linear", "Double"]:
            for i in self.hm.array:
                if i is None:
                    continue
                else:
                    if i[1].find(keyword):
                        l.append(i[0])
            return l
        
        elif self.hm.collision_type == "Chain":
            for i in self.hm.array:
                if i is None:
                    continue
                else:
                    for j in i:
                        if j[1].find(keyword):
                            l.append(j[0])
            return l
    
    def print_books(self):
        if self.hm.collision_type in ["Linear", "Double"]:
            for i in self.hm.array:
                if i is None:
                    continue
                
                else:
                    print(i[0] + ":", str(i[1]))
                    
        elif self.hm.collision_type == "Chain":
            for i in self.hm.array:
                if i is None:
                    continue
                for j in i:
                    print(j[0] + ":", str(j[1]))