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
    print(positions)
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
        new_lazor = Lazor(self.position, self.vector)
        Lazor_list.append(new_lazor)
        x_vec = self.vector[0]
        self.vector = (-x_vec, self.vector[1])
        # generate new lazor with new position and vector

    def refract_y(self):
        new_lazor = Lazor(self.position, self.vector)
        Lazor_list.append(new_lazor)
        x_vec = self.vector[0]
        self.vector = (-x_vec, self.vector[1])

    def absorb(self):
        self.vector = (0, 0)

lazor_1 = [(2, 7), (1, -1)]
lazor_2 = [(3, 2), (-1, -1)]

lazor_list = []
Lazor_list = []
lazor_list.append(lazor_1)
lazor_list.append(lazor_2)
for lazor in lazor_list:
    lazor_obj = Lazor(lazor[0], lazor[1])
    Lazor_list.append(lazor_obj)

if __name__ == "__main__":
    lazor_movement(grid, Lazor_list)
