'''
this will be the logic of how a lazor trail moves in a 2D grid
There are block positions in the grid that are occupied by objects
The lazor will move in a straight line until it hits a block
The block will reflect the lazor in a certain direction
The lazor will then continue in that direction until it hits another block or the target
the lazor target and the lazor origin exist in a space between block positions

lazors have two vectors, one for the x axis and one for the y axis
the lazor vectors can only be 1 or -1
if more x distance than y distance is covered before hitting a reflector, the x direction will reverse
if more y distance than x distance is covered before hitting a reflector, the y direction will reverse

0 = x = no block allowed
1 = lazor position, no block allowed
2 = o = blocks allowed
3 = A = fixed reflecting block
4 = B = fixed opaque block
5 = C = fixed refracting block

these blocks can occupy the 2 position:
6 = a = movable reflecting block
7 = b = movable opaque block
8 = c = movable refracting block

9 = lazor target, no block allowed
10 = lazor origin, no block allowed

Input:
data = {'grid': grid, 'blocks': blocks, 'lazers': lazers, 'points': points}
grid = nested lists
blocks = dictionary
lasers = nested tuples in list
points = nested tuples in list

'''
import copy
import time
import itertools
from bff_reader import read_bff
from lazor_output import visual_board


def lazor_movement(grid, lazor_objs):
    '''
    This is a function that will act as the lazor path
    the function will check all squares in the path of the lazor
    
    inputs = grid, lazor list (a list of Lazor objects)
    outputs = lazor path in a list of positions
    '''
    positions = []
    new_lazors = []
    for lazor in lazor_objs:
        current_positions = []
        start = lazor.position
        current_positions.append(start)
        new_pos = start
        # go through the loop to create a list of lazor positions for each lazor
        while len(current_positions) > 0 and len(current_positions) < 500:
            # check positions in the lazor path in which the lazor will encounter a block
            x_check = (new_pos[0] + lazor.vector[0], new_pos[1])
            y_check = (new_pos[0], new_pos[1] + lazor.vector[1])
            
            if x_check[0] < 0 or x_check[0] >= len(grid[0]) or x_check[1] < 0 or x_check[1] >= len(grid):
                break
            elif y_check[0] < 0 or y_check[0] >= len(grid[0]) or y_check[1] < 0 or y_check[1] >= len(grid):
                break
            x_blk = grid[x_check[1]][x_check[0]]
            y_blk = grid[y_check[1]][y_check[0]]
            # check to see if the lazor encounters a reflecting block
            if x_blk == 3 or x_blk == 6:
                lazor.reflect_x()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                current_positions.append(new_pos)
                continue
            elif y_blk == 3 or y_blk == 6:
                new_lazor = lazor.reflect_y()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                current_positions.append(new_pos)
                continue
            # check to see if the lazor encounters an opaque block
            elif x_blk == 4 or x_blk == 7:
                current_positions.append(new_pos)
                break
            elif y_blk == 4 or y_blk == 7:
                current_positions.append(new_pos)
                break
            # check to see if the lazor encounters a refracting block
            elif x_blk == 5 or x_blk == 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                new_lazor = lazor.refract_x(new_pos)
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                current_positions.append(new_pos)
                new_lazors.append(new_lazor)
                continue
            elif y_blk == 5 or y_blk == 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                new_lazor = lazor.refract_y(new_pos)
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                current_positions.append(new_pos)
                new_lazors.append(new_lazor)
                continue

            # break the loop when lazor reaches the end of the grid
            else:
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                if new_pos[0] < 0 or new_pos[0] >= len(grid[0]) or new_pos[1] < 0 or new_pos[1] >= len(grid[0]):
                    break
                else:
                    current_positions.append(new_pos)
                    continue
        positions.append(current_positions)

    return (positions,new_lazors)

# class to define lazor behaviour
class Lazor:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector
        self.og_vector = vector

    def set_position(self, position):
        self.position = position

    def reset_vector(self):
        self.vector = self.og_vector

    def reflect_x(self):
        x_vec = self.vector[0]
        self.vector = (-x_vec, self.vector[1])

    def reflect_y(self):
        y_vec = self.vector[1]
        self.vector = (self.vector[0], -y_vec)

    def refract_x(self, new_pos):
        x_vec = self.vector[0]
        new_lazor = Lazor(new_pos, (-x_vec, self.vector[1]))
        return new_lazor

    def refract_y(self, new_pos):
        y_vec = self.vector[1]
        new_lazor = Lazor(new_pos, (self.vector[0], - y_vec))
        return new_lazor
    
    def absorb(self,new_pos):
        self.vector = (0, 0)
        new_lazor = Lazor(new_pos, self.vector)
        return new_lazor

    def copy(self):
        return Lazor(self.position, self.vector)

# class to define block behaviour
class Block:
    def __init__(self, type):
        self.type = type
        self.position = None
        
    def clear(self):
        self.position = None

    def __repr__(self):
        return f"Block(type={self.type}, position={self.position})"

# create a function to generate all possible block positions
def block_positions(grid, block_list):
    available_positions = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 2:
                # Check that the cell is empty and add it to the list of available positions
                available_positions.append((row_idx, col_idx))
    
    block_types = []
    for block in block_list:
        block_types.append(block.type)
    if all(types ==block_types[0] for types in block_types):
        block_positions = []
        for positions in itertools.combinations(available_positions, len(block_list)):
            if len(set(positions)) == len(block_list):
                block_positions.append(list(positions))
    else:
        block_positions = []
        for positions in itertools.permutations(available_positions, len(block_list)):
            if len(set(positions)) == len(block_list):
                block_positions.append(list(positions))

    return block_positions



def has_nested_lists(lst):
    """
    Returns True if the list `lst` contains nested lists, False otherwise.
    """
    for item in lst:
        if isinstance(item, list):
            return True
    return False

def solve_puzzle(grid, lazor_objs, block_config, target_list, block_objs):
    new_grid = copy.deepcopy(grid)
    for (block_posi, block) in itertools.zip_longest(block_config, block_objs):

        block.position = block_posi

        if block.type == 'a':
            new_grid[block.position[0]][block.position[1]] = 6
        elif block.type == 'b':
            new_grid[block.position[0]][block.position[1]] = 7
        elif block.type == 'c':
            new_grid[block.position[0]][block.position[1]] = 8

    lazor_data = lazor_movement(new_grid, lazor_objs)
    lazor_positions = (lazor_data[0])
    all_positions = []
    new_lazors = lazor_data[1]

    if has_nested_lists(lazor_positions):
        for eleme in lazor_positions:
            for elem in eleme:
                all_positions.append(elem)

    if len(new_lazors) > 0:
        refract_lazors = lazor_movement(new_grid, new_lazors)
        for element in refract_lazors[0]:
            if len(element) > 0:
                lazor_positions.append(element)
                for i in range(len(element)):
                    all_positions.append(element[i])
    for lazor in lazor_objs:
        lazor.reset_vector()

    if all(elem in all_positions for elem in target_list):
        return (True, lazor_positions, new_grid)
    else:
        for block in block_objs:
            block.clear()
            return False

def solver(filename):
    '''
    hi
    '''
    data = read_bff(filename)
    grid = data['grid']

    # Convert grid to numbered syntax
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == 'o':
                grid[y][x] = 2
            elif grid[y][x] == ' ':
                grid[y][x] = 1
            elif grid[y][x] == 'x':
                grid[y][x] = 0
            elif grid[y][x] == 'A':
                grid[y][x] = 3
            elif grid[y][x] == 'B':
                grid[y][x] = 4
            elif grid[y][x] == 'C':
                grid[y][x] = 5

    # create a list of lazor targets
    targets = data['points']

    # initialize block data
    blocks = data['blocks']
    block_list = []

    # Created block list 
    for element in blocks:
        number_of_blocks = blocks[element]
        if len(number_of_blocks) > 0:
            for u in range(number_of_blocks[0]):
                block_list.append(element)

    # created block object list
    block_objects = []
    for block in block_list:
        block_obj = Block(block)
        block_objects.append(block_obj)

    # Accesses the lazor data
    lazors = data['lazers']
    lazor_list = []

    for lazor in lazors:
        lazor_data = []
        initial_position = (lazor[0],lazor[1])
        lazor_data.append(initial_position)
        initial_vector = (lazor[2],lazor[3])
        lazor_data.append(initial_vector)
        lazor_list.append(lazor_data)

    lazor_objects = []
    for lazor in lazor_list:
        lazor_obj = Lazor(lazor[0], lazor[1])
        lazor_objects.append(lazor_obj)
    
    block_pos = block_positions(grid, block_objects)
    for block_config in block_pos:
        solved = solve_puzzle(grid, lazor_objects, block_config, targets, block_objects)
        if solved:
            lazor_positions = solved[1]
            new_grid = solved[2]
            solved_data = {}
            # Convert grid to numbered syntax
            for y in range(len(new_grid)):
                for x in range(len(new_grid[0])):
                    if new_grid[y][x] == 2:
                        new_grid[y][x] = 'o'
                    elif new_grid[y][x] == 1:
                        new_grid[y][x] = ' '
                    elif new_grid[y][x] == 0:
                        new_grid[y][x] = 'x'
                    elif new_grid[y][x] == 3:
                        new_grid[y][x] = 'A'
                    elif new_grid[y][x] == 4:
                        new_grid[y][x] = 'B'
                    elif new_grid[y][x] == 5:
                        new_grid[y][x] = 'C'
                    elif new_grid[y][x] == 6:
                        new_grid[y][x] = 'a'
                    elif new_grid[y][x] == 7:
                        new_grid[y][x] = 'b'
                    elif new_grid[y][x] == 8:
                        new_grid[y][x] = 'c'
            solved_data['grid'] = new_grid
            solved_data['points'] = targets
            solved_data['lazors'] = lazor_positions
            solved_data['filename'] = filename
            visual_board(solved_data)
            break
        else:
            block_pos.pop(0)
            continue

if __name__ == "__main__":
    
    startTime = time.time()
    solver('dark_1.bff')
    solver('mad_1.bff')
    solver('mad_4.bff') 
    solver('mad_7.bff') 
    solver('numbered_6.bff') 
    solver('showstopper_4.bff')
    solver('tiny_5.bff')
    solver('yarn_5.bff') 
    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str((executionTime)))
