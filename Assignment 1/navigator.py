from maze import *
from exception import *
from stack import *
class PacMan:
    def __init__(self, grid : Maze) -> None:
        ## DO NOT MODIFY THIS FUNCTION
        self.navigator_maze = grid.grid_representation
    def find_path(self, start, end):
        # IMPLEMENT FUNCTION HERE
        if self.navigator_maze[start[0]][start[1]] == 1: raise PathNotFoundExcepction
        grid = Maze(len(self.navigator_maze), len(self.navigator_maze[0]))
        grid.grid_representation = self.navigator_maze
        stk = Stack()
        blacklist = Stack()
        current = start
        while current != end:
            if current not in stk.stack:
                stk.push(current)
                blacklist.push([])
            nbrs = grid.neighbours(current)
            nbrs_values = []
            for i in nbrs:
                if grid.is_ghost(i[0], i[1]): nbrs_values.append(1)
                else: nbrs_values.append(0)
                
            if 0 not in nbrs_values:
                blacklist.stack.pop()
                if len(stk.stack) == 1: raise PathNotFoundException
                blacklist.stack[-1].append(stk.stack.pop())
                current = stk.peek()
            else:
                for i in range(len(nbrs)):
                    if nbrs_values[i] != 1 and nbrs[i] not in blacklist.peek() and nbrs[i] not in stk.stack:
                        current = nbrs[i]
                        break
                else:
                    blacklist.stack.pop()
                    if len(stk.stack) == 1: raise PathNotFoundException
                    blacklist.stack[-1].append(stk.stack.pop())
                    current = stk.peek()
        stk.push(current)
        return stk.stack