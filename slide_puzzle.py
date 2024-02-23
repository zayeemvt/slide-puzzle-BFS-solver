import numpy as np
import copy
from collections import deque

# Reference solution matrix
solution = np.array([[1,2,3],[4,5,6],[7,8,0]])


# Randomly generate a puzzle configuration
def generate_puzzle() -> np.array:
    puzzle = np.arange(9)
    np.random.shuffle(puzzle)
    puzzle = puzzle.reshape((3,3))
    return puzzle


# Return row and column of blank tile in puzzle
def find_blank_tile(puzzle):
    location = np.where(puzzle == 0)
    return location[0][0], location[1][0]


# Returns a copy of the puzzle with the blank tile slid in the specified direction
# Returns None if move is invalid
def slide_blank_tile(puzzle, dir: str) -> np.array:
    puzzle = copy.deepcopy(puzzle)

    dir = dir.lower() # in case of typos

    row, col = find_blank_tile(puzzle)
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
        return None
    
    dest_row = row + row_offset
    dest_col = col + col_offset

    puzzle[row][col] = puzzle[dest_row][dest_col] # replace blank with the destination tile
    puzzle[dest_row][dest_col] = 0 # replace destination tile with the blank
    return puzzle



# Storage class used to navigate the breadth-first search tree
class Node:
    def __init__(self, parent_index, puzzle: np.array, move: str = None):
        self.parent_index = parent_index
        self.puzzle = puzzle
        self.move = move

    def __str__(self):
        return str(self.puzzle)
    


# Function that solves a puzzle
def solvePuzzle(initial):
    directions = ['left', 'up', 'right', 'down']

    node_list = []
    itr = 0

    root_node = Node(None, initial)
    node_list.append(root_node)

    solved = False
    
    # Iterate through the node list until puzzle is solved or the list is exhausted
    while (not solved and itr < len(node_list)):
        current_node = node_list[itr]

        # Explore the puzzle states from pushing the blank tile in each direction
        for dir in directions:
            duplicate_node = False
            new_puzzle = slide_blank_tile(current_node.puzzle, dir)
            # print(f'Checking:\n{new_puzzle}')

            # If invalid move, skip this attempt
            if new_puzzle is None:
                # print("Invalid. Moving on...")
                continue

            # Search for duplicate nodes
            for i in range(0,len(node_list)):
                if np.array_equal(node_list[i].puzzle, new_puzzle) and i != itr:
                    duplicate_node = True
                    # print(f'Duplicate found:\n{node_list[i].puzzle}')
                    break
            
            # If no duplicates, add to list and check for game solve
            if not duplicate_node:
                node_list.append(Node(itr,new_puzzle,dir))
                # print(f'No duplicates found. Added.')

                if np.array_equal(solution, new_puzzle):
                    solved = True
                    break
            
        itr += 1
        print(f'{itr} nodes visited, {len(node_list) - itr} nodes left')

    
    if solved:
        move_sequence = []

        end_node = node_list[-1]
        move = end_node.move
        parent_node = end_node # Initialize the parent node
        
        while (not move is None): # Run until initial game state is reached
            move_sequence.append(move)
            parent_node = node_list[parent_node.parent_index] # Get the current node's parent
            move = parent_node.move

        move_sequence.reverse()
        print(move_sequence)





# Reverse solution
myPuzzle = copy.copy(solution)
sequence = ['left', 'left', 'up', 'right', 'right', 'up', 'left', 'left', 'down', 'right', 'up', 'right', 'down']
for move in sequence:
    myPuzzle = slide_blank_tile(myPuzzle, move)


# Simple puzzle
# myPuzzle = np.array([[0,3,6],[1,7,2],[5,4,8]])

# Purely random, takes very long time to solve
# myPuzzle = np.array([[3,4,1],[6,0,2],[7,8,5]])

print(myPuzzle)
solvePuzzle(myPuzzle)