from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        self.bins_id = AVLTree()
        self.bins_cap = AVLTree()
        self.obj_tree = AVLTree()
        self.bins = 0
        self.objects = 0
        
    def add_bin(self, bin_id, capacity):
        bin1 = Bin(bin_id, capacity)
        self.bins_cap.insert_value((bin1.capacity, bin1.bin_id), bin1)
        self.bins_id.insert_value((bin1.bin_id, None), bin1)
        self.bins += 1
        
    def add_object(self, object_id, size, color):
        obj = Object(object_id, size, color)
        
        if color == Color.BLUE:
            bin1 = self.bins_cap._compact_fit(self.bins_cap.root, size)
        elif color == Color.YELLOW:
            temp = self.bins_cap.root
            node = self.bins_cap._compact_fit(self.bins_cap.root, size)
            if node is None:
                bin1 = None
            else:
                bin1 = self.bins_cap._lcgi(temp, node.key[0])
        elif color == Color.RED:
            node = self.bins_cap._largest_fit(self.bins_cap.root, size)
            if node is None:
                bin1 = None
            else:
                bin1 = self.bins_cap._gcli(self.bins_cap.root, node.key[0])
        elif color == Color.GREEN:
            bin1 = self.bins_cap._largest_fit(self.bins_cap.root, size)
            
        if bin1 is None: raise NoBinFoundException
        
        x = bin1.data
        
        self.bins_cap.delete_value((x.capacity, x.bin_id))
        
        x.add_object(obj)
        self.bins_cap.insert_value((x.capacity, x.bin_id), x)
        self.obj_tree.insert_value((object_id, None), obj)
        self.objects += 1
        
    def delete_object(self, object_id):
        obj = self.obj_tree.search(self.obj_tree.root, (object_id, None))
        if obj is None: return None
        bin1 = obj.bin
        self.bins_cap.delete_value((bin1.capacity, bin1.bin_id))
        bin1.remove_object(object_id)
        self.bins_cap.insert_value((bin1.capacity, bin1.bin_id), bin1)
        self.obj_tree.delete_value((object_id, None))
        
        
    def bin_info(self, bin_id):
        bin1 = self.bins_id.search((bin_id, None))
        return (bin1.capacity, bin1.objects.inorder_traversal(bin1.objects.root))
    
    def object_info(self, object_id):
        obj = self.obj_tree.search((object_id, None))
        if obj is None: return None
        return obj.bin.bin_id