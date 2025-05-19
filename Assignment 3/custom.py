# You can add any additional function and class you want to implement in this file
class Empty(Exception):
    def __init__(self):
        super().__init__("The array is empty")

def comp_1(x, y):
    return x.load < y.load

def comp_2(x, y):
    return x[0] < y[0] if x[0] != y[0] else x[1].id < y[1].id