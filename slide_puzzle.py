import numpy as np
import copy
from collections import deque


solution = np.array([[1,2,3],[4,5,6],[7,8,0]])

class Puzzle:
    def __init__(self, grid = None):
        if (grid is None):
            self.grid = np.arange(9)
            np.random.shuffle(self.grid)
            self.grid = self.grid.reshape((3,3))
        else:
            self.grid = copy.copy(grid)
    
    def find_blank(self):
        location = np.where(self.grid == 0)
        return location[0][0], location[1][0]
    
    def slide(self, dir: str):
        dir = dir.lower()

        row, col = self.find_blank()
        row_offset = 0
        col_offset = 0

        if (dir == 'left' and col > 0):
            col_offset = -1
        elif (dir == 'right' and col < 2):
            col_offset = 1
        elif (dir == 'up' and row > 0):
            row_offset = -1
        elif (dir == 'down' and row < 2):
            row_offset = 1
        else:
            return False
        
        dest_row = row + row_offset
        dest_col = col + col_offset

        self.grid[row][col] = self.grid[dest_row][dest_col]
        self.grid[dest_row][dest_col] = 0
        return True

    def __str__(self):
        return str(self.grid)



class Node:
    def __init__(self, parent, puzzle: Puzzle, move: str = None):
        self.parent = parent
        self.puzzle = puzzle
        self.children = []
        self.move = move
    
    def add_child(self, dir: str):
        new_puzzle = Puzzle(self.puzzle.grid)

        if(new_puzzle.slide(dir)): # if successful move
            child = Node(self, new_puzzle, dir)
            self.children.append(child)
            return child
        else:
            return None
        
    def remove_last_child(self):
        del self.children[-1]

    def __str__(self):
        return str(self.puzzle)
    



def solvePuzzle(initial):
    directions = ['left', 'up', 'right', 'down']

    nodes_visited = deque()
    nodes_to_visit = deque()

    root_node = Node(None, initial)
    nodes_to_visit.append(root_node)

    solved = False
    
    while (not solved and len(nodes_to_visit) > 0):
        current_node = nodes_to_visit[0]

        for dir in directions:
            child_removed = False
            child = current_node.add_child(dir)

            if not child is None:
                for node in nodes_visited:
                    if np.array_equal(node.puzzle.grid, child.puzzle.grid):
                        current_node.remove_last_child()
                        child_removed = True
                        break
                
                if not child_removed:
                    for node in nodes_to_visit:
                        if np.array_equal(node.puzzle.grid, child.puzzle.grid):
                            current_node.remove_last_child()
                            child_removed = True
                            break

                if not child_removed:
                    nodes_to_visit.append(child)
                    if np.array_equal(solution, child.puzzle.grid):
                        solved = True
                        break
            
        nodes_visited.append(nodes_to_visit.popleft())
        print(f'{len(nodes_visited)} nodes visited, {len(nodes_to_visit)} nodes left')
    
    if solved:
        move_sequence = []

        move = child.move
        parent_node = child
        
        while (not move is None):
            move_sequence.append(move)
            parent_node = parent_node.parent
            move = parent_node.move

        move_sequence.reverse()
        print(move_sequence)







myPuzzle = Puzzle(np.array([[3,4,1],[6,0,2],[7,8,5]]))

myPuzzle = Puzzle(copy.copy(solution))
sequence = ['left', 'left', 'up', 'right', 'right', 'up', 'left', 'left', 'down', 'right', 'up', 'right', 'down']
for move in sequence:
    myPuzzle.slide(move)

print(myPuzzle)
solvePuzzle(myPuzzle)