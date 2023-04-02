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

rows = 8
columns = 8
grid = [[2 for x in range(columns)] for y in range(rows)]

for i in range(rows):
    for j in range(columns):
        if i % 2 == 0:
            grid[i][j] = 2 if j % 2 == 0 else 1
        else:
            grid[i][j] = 1


# set the target position and lazor origin
grid[2][7] = 10
grid[3][0] = 9
grid[4][3] = 9
grid[2][5] = 9
grid[4][7] = 9


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
        new_lazor = Lazor(self.position, self.vector)
        return new_lazor
    
    def refract_y(self):
        self.vector[0] = self.vector[0]
        self.vector[1] = -self.vector[1]
        # generate new lazor with new position and vector
        new_lazor = Lazor(self.position, self.vector)
        return new_lazor

    def absorb(self):
        self.vector[0] = 0
        self.vector[1] = 0

    def place_lazor(self, position, grid):
        self.position = position
        self.grid = grid
        grid[position[0]][position[1]] = 10

# start = lazor_position
# direction = lazor_vector

# function to move lazor to the last possible position
def lazor_movement(start, direction, grid):
    positions = []
    positions.append(start)
    while len(positions) > 0:
        # set bounds of positions
        next_position = (start[0] + direction[0], start[1] + direction[1])
        x_bound = len(grid[0])
        y_bound = len(grid)
        # check if a lazor passed through a block in the x direction
        x_check = (next_position[0] - direction[0], next_position[1])
        # check if a lazor passed through a block in the y direction
        y_check = (next_position[0], next_position[1] - direction[1])
        # check to see if the lazor is out of bounds
        if next_position[0] < 0 or next_position[0] >= y_bound or next_position[1] < 0 or next_position[1] >= x_bound:
            break
        # check to see if a block is encountered in the x_check position
        if grid[x_check[0]][x_check[1]] != 2:
            if grid[x_check[0]][x_check[1]] == 3:
                direction = (-direction[0], direction[1])
            elif grid[x_check[0]][x_check[1]] == 4:
                positions.append(x_check)
                break
            elif grid[x_check[0]][x_check[1]] == 5:
                direction = (-direction[0], direction[1])
                positions.append(x_check)
        # check to see if a block is encountered in the y_check position
        if grid[y_check[0]][y_check[1]] != 2:
            if grid[y_check[0]][y_check[1]] == 3:
                direction = (direction[0], -direction[1])
            elif grid[y_check[0]][y_check[1]] == 4:
                positions.append(y_check)
                break
            elif grid[y_check[0]][y_check[1]] == 5:
                direction = (direction[0], -direction[1])
                positions.append(y_check)
        start = next_position
        positions.append(start)
    print(positions)
    return positions

if __name__ == '__main__':
    lazor_movement((2, 7), (1, -1), grid)
    print(grid)