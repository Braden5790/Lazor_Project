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

0 = no block allowed
1 = lazor position, no block allowed
2 = blocks allowed
3 = fixed reflecting block
4 = fixed opaque block
5 = fixed refracting block

these blocks can occupy the 2 position:
6 = movable reflecting block
7 = movable opaque block
8 = movable refracting block

9 = lazor target, no block allowed
10 = lazor origin, no block allowed
'''

import itertools

grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]]

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
        while len(positions) > 0 and len(positions) < 500:
            # check positions in the lazor path in which the lazor will encounter a block
            x_check = (new_pos[0] + lazor.vector[0], new_pos[1])
            y_check = (new_pos[0], new_pos[1] + lazor.vector[1])
            if x_check[0] < 0 or x_check[0] >= len(grid) or x_check[1] < 0 or x_check[1] >= len(grid):
                break
            elif y_check[0] < 0 or y_check[0] >= len(grid) or y_check[1] < 0 or y_check[1] >= len(grid):
                break
            x_blk = grid[x_check[0]][x_check[1]]
            y_blk = grid[y_check[0]][y_check[1]]
            # print(positions)
            # check to see if the lazor encounters a reflecting block
            if x_blk == 3 or x_blk == 6:
                lazor.reflect_x()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                lazor.set_position(new_pos)
                print("x-reflect!")
                continue
            elif y_blk == 3 or y_blk == 6:
                lazor.reflect_y()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                lazor.set_position(new_pos)
                print("y-reflect!")
                continue
            # check to see if the lazor encounters an opaque block
            elif x_blk == 4 or x_blk == 7:
                # in the x_check position, the lazor's last position is the x_check position
                lazor.absorb()
                # break loop since lazor is absorbed
                break
            elif y_blk == 4 or y_blk == 7:
                # in the y_check position, the lazor's last position is the y_check position
                lazor.absorb()
                # break loop since lazor is absorbed
                break
            # check to see if the lazor encounters a refracting block
            elif x_blk == 5 or x_blk == 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                lazor.refract_x()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                lazor.set_position(new_pos)
                print("x-fract!")
                print(lazor.position)
                continue
            elif y_blk == 5 or y_blk == 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                lazor.refract_y()
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                positions.append(new_pos)
                lazor.set_position(new_pos)
                print("y-fract!")
                continue
            # continue for all other cases
            # break the loop when lazor reaches the end of the grid
            else:
                new_pos = (new_pos[0] + lazor.vector[0], new_pos[1] + lazor.vector[1])
                lazor.set_position(new_pos)
                if new_pos[0] < 0 or new_pos[0] >= len(grid) or new_pos[1] < 0 or new_pos[1] >= len(grid):
                    break
                else:
                    positions.append(new_pos)
                    continue
    # print(positions)
    return positions

# class to define lazor behaviour
class Lazor:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector

    def set_position(self, position):
        self.position = position

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
    
    def copy(self):
        return Lazor(self.position, self.vector)


# class to define block behaviour
class Block:
    def __init__(self, type):
        self.type = type
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
    
    # Generate all possible permutations of block positions
    block_positions = []
    for positions in itertools.permutations(available_positions, len(block_list)):
        # Check if any two blocks occupy the same position
        if len(set(positions)) == len(block_list):
            block_positions.append(list(positions))
    # print(block_positions)
    return block_positions


def solve_puzzle(grid, lazor_list, block_config, target_list, block_list):
    # block_arr = block_list[0]
    for block_posi, block in zip(block_config, block_list):
        block.position = block_posi
        grid[block.position[0]][block.position[1]] = block.type
        if block.type == 'a':
            grid[block.position[0]][block.position[1]] = 6
        elif block.type == 'b':
            grid[block.position[0]][block.position[1]] = 7
        elif block.type == 'c':
            grid[block.position[0]][block.position[1]] = 8

    lazor_positions = lazor_movement(grid, lazor_list)
    print(lazor_positions)
    # Check if all target positions are hit
    if all(elem in lazor_positions for elem in target_list) is True:
        print("Solution found!")
        print(lazor_positions)
        print(grid)
        return True
    else:
        # print("Solution not found!")
        return False

def solver(grid, lazor_list, block_list, target_list):
    block_pos = block_positions(grid, block_list)
    for block_config in block_pos:
        fu = solve_puzzle(grid, lazor_list, block_config, target_list, block_list)
        if fu == True:
            return block_config
        else:
            block_pos.pop(0)
            continue


lazor_1 = [(2, 7), (1, -1)]
# lazor_2 = [(3, 2), (-1, -1)]

lazor_list = []
Lazor_list = []
lazor_list.append(lazor_1)
# lazor_list.append(lazor_2)
for lazor in lazor_list:
    a, b = lazor[0]
    lazor_pos = (b, a)
    x, y = lazor[1]
    lazor_vec = (y, x)
    lazor_obj = Lazor(lazor_pos, lazor_vec)
    Lazor_list.append(lazor_obj)

block_list = ['a', 'a', 'c']
Block_list = []
for block in block_list:
    block_obj = Block(block)
    Block_list.append(block_obj)

target_list = []
raw_target_list = [(3, 0), (4, 3), (2, 5), (4, 7)]
for target in raw_target_list:
    a, b = target
    new_target = (b, a)
    target_list.append(new_target)

if __name__ == "__main__":
    solver(grid, Lazor_list, Block_list, target_list)
    # print(block_positions(grid, Block_list))