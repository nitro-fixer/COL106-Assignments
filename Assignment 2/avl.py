from node import Node
from object import Object

def comp_1(node_1, node_2):
    if node_1.key[0] == node_2.key[0]:
        if node_1.key[1] > node_2.key[1]:
            return 1
        elif node_1.key[1] < node_2.key[1]:
            return -1
    elif node_1.key[0] > node_2.key[0]:
        return 1
    elif node_1.key[0] < node_2.key[0]:
        return -1
        
class AVLTree:
    def __init__(self, compare_function=comp_1):
        self.root = None
        self.size = 0
        self.comparator = compare_function
        
    def height(self, node):
        if not node:
            return 0
        return node.height
    
    def balance(self, node):
        if not node:
            return 0
        return self.height(node.left) - self.height(node.right)
    
    def update_height(self, node):
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))
            
    def left_rotate(self, z):
        y = z.right
        T3 = y.left
        
        y.left = z
        z.right = T3
        
        self.update_height(z)
        self.update_height(y)
        return y
    
    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        
        y.right = z
        z.left = T3
        
        self.update_height(z)
        self.update_height(y)
        return y
    
    def balance_avl(self, node):
        self.update_height(node)
        balance_factor = self.balance(node)
        
        #Right heavy
        if balance_factor < -1:
            if self.balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
                
            return self.left_rotate(node)
            
        #Left heavy
        if balance_factor > 1:
            if self.balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
            
            return self.right_rotate(node)
            
        return node
    
    def _insert(self, root, key, data):
        if root is None:
            return Node(key, data)
        
        if self.comparator(root, Node(key, data)) == 1:
            root.left = self._insert(root.left, key, data)
        else:
            root.right = self._insert(root.right, key, data)
            
        self.update_height(root)
        return self.balance_avl(root)
    
    def _delete(self, root, key):
        if root is None: return None
        
        if self.comparator(root, Node(key, None)) == 1:
            root.left = self._delete(root.left, key)
        elif self.comparator(root, Node(key, None)) == -1:
            root.right = self._delete(root.right, key)
        else:
            if root.right is None: return root.left
            if root.left is None: return root.right
            
            inorder_successor = self._minn(root.right)
            root.key = inorder_successor.key
            root.data = inorder_successor.data
            root.right = self._delete(root.right, inorder_successor.key)
            
        self.update_height(root)
        return self.balance_avl(root)
    
    def _minn(self, root):
        if root is None: 
            return root
        elif root.left is None:
            return root
        else:
            return self._minn(root.left)
    
    def inorder_traversal(self, root):
        if root is None: return []
        
        return self.inorder_traversal(root.left) + [root.key[0]] + self.inorder_traversal(root.right)
    
    
    def _search(self, root, key):
        if root is None: return None
        
        if root.key == key:
            return root.data
        elif self.comparator(root, Node(key, None)) == 1:
            return self._search(root.left, key)
        return self._search(root.right, key)
    
    def _lcgi(self, node, value):
        result = None
        
        while node is not None:
            if node.key[0] <= value:
                result = node
                node = node.right
            else:
                node = node.left
                
        return result
    
    def _gcli(self, node, value):
        result = None
        
        while node is not None:
            if node.key[0] >= value:
                result = node
                node = node.left
            else:
                node = node.right
        
        return result
    
    def _compact_fit(self, root, x):
        result = None
        
        while root is not None:
            if root.key[0] < x:
                root = root.right
            else:
                if result is None or root.key[0] < result.key[0] or (root.key[0] == result.key[0] and root.key[1] < result.key[1]):
                    result = root
                root = root.left
        
        return result
    
    def _largest_fit(self, root, x):
        if root is None: return None
        
        if root.right is None:
            if root.key[0] < x: return None
            return root
        else:
            return self._largest_fit(root.right, x)
        
    
    def insert_value(self, key, data):
        self.root = self._insert(self.root, key, data)
        self.size += 1
        
    def delete_value(self, key):
        if self.root is None: return
        self.root = self._delete(self.root, key)
        if self.root is not None:
            self.size -= 1
            
    def search(self, key):
        return self._search(self.root, key)