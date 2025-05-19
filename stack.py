class Stack:
    def __init__(self) -> None:
        #YOU CAN (AND SHOULD!) MODIFY THIS FUNCTION
        self.stack = []
    # You can implement this class however you like
    def push(self, pos) -> None:
        self.stack.append(pos)
        
    def peek(self):
        return self.stack[-1]
        
    def clear(self) -> None:
        self.stack = []
        
    def is_empty(self) -> bool:
        if len(self.stack) == 0: return True
        return False