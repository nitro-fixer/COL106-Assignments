from avl import AVLTree
from object import Object

class Bin:
    def __init__(self, bin_id, capacity):
        self.bin_id = bin_id
        self.capacity = capacity
        self.objects = AVLTree()
        
    def add_object(self, object):
        self.objects.insert_value((object.object_id, None), object)
        self.capacity -= object.size
        object.bin = self
        
    def remove_object(self, object_id):
        obj = self.objects.search(self.objects.root, (object_id, None))
        if obj is None: return None
        self.capacity += obj.size
        self.objects.delete_value((object_id, None))