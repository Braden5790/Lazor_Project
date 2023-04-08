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
from bff_reader import read_bff
import random

data = read_bff('mad_1.bff')
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

# add targets to grid denoting lazor targets with 9
for target in targets:
    grid[target[0]][target[1]] = 9

def lazor_movement(grid, Lazor_list):
    '''
    This is a function that will act as the lazor path
    the function will check all squares in the path of the lazor
    
    inputs = grid, lazor list (a list of Lazor objects)
    outputs = lazor path in a list of positions
    '''
    positions = []
    for lazor in Lazor_list:
        lp = lazor.position
        start = lp
        positions.append(start)
        new_pos = start
        # go through the loop to create a list of lazor positions for each lazor
        while len(positions) > 0:
            # check positions in the lazor path in which the lazor will encounter a block
            x_check = (new_pos[0] + lazor.vector[0], new_pos[1])
            y_check = (new_pos[0], new_pos[1] + lazor.vector[1])
            if x_check[0] < 0 or x_check[0] >= len(grid) or x_check[1] < 0 or x_check[1] >= len(grid):
                break
            elif y_check[0] < 0 or y_check[0] >= len(grid) or y_check[1] < 0 or y_check[1] >= len(grid):
                break
            x_blk = grid[x_check[0]][x_check[1]]
            y_blk = grid[y_check[0]][y_check[1]]
            print(positions)
            # check to see if the lazor encounters a reflecting block
            if x_blk == 3 or x_blk == 6:
                lazor.reflect_x()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                continue
            elif y_blk == 3 or y_blk == 6:
                lazor.reflect_y()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                continue
            # check to see if the lazor encounters an opaque block
            elif x_blk == 4 or x_blk == 7:
                # in the x_check position, the lazor's last position is the x_check position
                lazor.absorb()
                new_pos = x_check
                positions.append(new_pos)
                # break loop since lazor is absorbed
                break
            elif y_blk == 4 or y_blk == 7:
                # in the y_check position, the lazor's last position is the y_check position
                lazor.absorb()
                new_pos = y_check
                positions.append(new_pos)
                # break loop since lazor is absorbed
                break
            # check to see if the lazor encounters a refracting block
            elif x_blk == 5 or x_blk == 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                lazor.refract_x()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                continue
            elif y_blk == 5 or y_blk == 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                lazor.refract_y()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                continue
            # continue for all other cases
            # break the loop when lazor reaches the end of the grid
            else:
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                if new_pos[0] < 0 or new_pos[0] >= len(grid) or new_pos[1] < 0 or new_pos[1] >= len(grid):
                    break
                else:
                    positions.append(new_pos)
                    continue
    return positions

# class to define lazor behaviour
class Lazor:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector

    def reflect_x(self):
        x_vec = self.vector[0]
        self.vector = (-x_vec, self.vector[1])

    def reflect_y(self):
        y_vec = self.vector[1]
        self.vector = (self.vector[0], -y_vec)

    def refract_x(self):
        x_vec = self.vector[0]
        new_pos = (self.position[0] - x_vec, self.position[1] + self.vector[1])
        new_lazor = Lazor(new_pos, (-x_vec, self.vector[1]))
        Lazor_list.append(new_lazor)

    def refract_y(self):
        y_vec = self.vector[1]
        new_pos = (self.position[0] + self.vector[0], self.position[1] - y_vec)
        new_lazor = Lazor(new_pos, (self.vector[0], - y_vec))
        Lazor_list.append(new_lazor)

    def absorb(self):
        self.vector = (0, 0)


# class to define block behaviour
class Block:
    def __init__(self, type):
        self.type = type
        self.position = None
        
    def place_on_grid(self, grid):
        available_positions = []
        for row_idx, row in enumerate(grid):
            for col_idx, cell in enumerate(row):
                if cell == 2:
                    # Check that the cell is empty and that an 'a' block can only be placed on even columns
                    available_positions.append((row_idx, col_idx))
        if available_positions:
            self.position = random.choice(available_positions)
            grid[self.position[0]][self.position[1]] = self.type
            if self.type == 'a':
                grid[self.position[0]][self.position[1]] = 6
            elif self.type == 'b':
                grid[self.position[0]][self.position[1]] = 7
            elif self.type == 'c':
                grid[self.position[0]][self.position[1]] = 8
            return True
        else:
            return False
    
    def __eq__(self, other):
        return self.type == other.type
    
    def __repr__(self):
        return f"Block(type={self.type}, position={self.position})"


def solve_blocks(Block_list, grid, target_list):
    '''
    This function will place the blocks in the grid
    '''

    cache = []
    true_list = [False]
    
    while all(true_list) == False:
        # Cache the position of the block arrangement for all blocks
        inner_cache = []
        for block in Block_list:
            block.place_on_grid(grid)
            inner_cache.append(block.position)
            print(block.position)
        if inner_cache in cache:
            continue
        else:
            cache.append(inner_cache)
        positions = lazor_movement(grid, Lazor_list)
        print(cache)
        if all(elem in positions for elem in target_list) is True:
            true_list = [True]
            print(positions)
            print(target_list)
        else:
            continue
    print("you are so good")


lazor_1 = [(2, 7), (1, -1)]
lazor_2 = [(3, 2), (-1, -1)]

lazor_list = []
Lazor_list = []
lazor_list.append(lazor_1)
lazor_list.append(lazor_2)
for lazor in lazor_list:
    lazor_obj = Lazor(lazor[0], lazor[1])
    Lazor_list.append(lazor_obj)

block_list = ['a', 'a', 'c']
Block_list = []
for block in block_list:
    block_obj = Block(block)
    Block_list.append(block_obj)

target_list = [(3, 0), (4, 3), (2, 5), (4, 7)]

if __name__ == "__main__":
    solve_blocks(Block_list, grid, target_list)
    # lazor_movement(grid, Lazor_list)
    # print(grid)
