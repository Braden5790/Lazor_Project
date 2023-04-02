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
'''

# create a 2D array to represent the grid
# the grid will be a 2D list
# the dimension of the grid will be set by a dimension size

# # create a function to make an empty grid
# def create_grid(dimension):
#     grid = []
#     for i in range(dimension):
#         grid.append([])
#         for j in range(dimension):
#             grid[i].append(0)
#     return grid

# # for all odd numbers, set the grid position to 1
# def set_target(grid):
#     for i in range(len(grid)):
#         for j in range(len(grid)):
#             if i % 2 != 0 and j % 2 != 0:
#                 grid[i][j] = 1
#     print(grid)
#     return grid

grid = [[2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2]]

grid[2][7] = 
grid[3][0] = 9


# the lazor will be a 2D list
# the lazor will be 2x2
# the lazor will be a list of coordinates
# the lazor will be a list of vectors
lazor = (
    [[2, 7], [1, -1]])

# create logic for lazor movement
# create logic for lazor reflection
# create logic for lazor refraction
# create logic for lazor absorption

# class to define lazor behaviour
class Lazor:
    def __init__(self, position, vector):
        self.position = position
        self.vector = vector

    def add_lazor(self, position, vector):
        self.position = position
        self.vector = vector

    def reflect_x(self):
        self.vector[0] = -self.vector[0]
        self.vector[1] = self.vector[1]

    def reflect_y(self):
        self.vector[0] = self.vector[0]
        self.vector[1] = -self.vector[1]

    def refract_x(self):
        self.vector[0] = -self.vector[0]
        self.vector[1] = self.vector[1]
        # generate new lazor with new position and vector
        new_lazor = Lazor.add_lazor(self, self.position, self.vector)
        return new_lazor
    
    def refract_y(self):
        self.vector[0] = self.vector[0]
        self.vector[1] = -self.vector[1]
        # generate new lazor with new position and vector
        new_lazor = Lazor.add_lazor(self, self.position, self.vector)
        return new_lazor

    def absorb(self):
        self.vector[0] = 0
        self.vector[1] = 0

# start = lazor_position
# direction = lazor_vector

# lazor will hit the 
def lazor_movement(start, direction):
    next_position = start + direction
    # check if a lazor passed through a block
    x_check = (0, 0)
    x_check[0] = next_position[0] - direction[0]
    x_check[1] = next_position[1]
    # check to see if x_check is a block
    if grid[x_check[0]][x_check[1]] == A:
        Lazor.reflect(lazor)

    


if __name__ == '__main__':
    grid = create_grid(4)
    grid = set_target(grid)


