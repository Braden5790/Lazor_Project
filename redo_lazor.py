rows = 8
columns = 8
grid = [[2 for x in range(columns + 1)] for y in range(rows + 1)]

for i in range(rows + 1):
    for j in range(columns + 1):
        if i % 2 != 0:
            grid[i][j] = 2 if j % 2 != 0 else 1
        else:
            grid[i][j] = 1

# set the target position and lazor origin

grid[3][0] = 9
grid[4][3] = 9
grid[2][5] = 9
grid[4][7] = 9

# create a list of lazor targets
targets = [(3, 0), (4, 3), (2, 5), (4, 7)]

# add targets to grid denoting lazor targets with 9
for target in targets:
    grid[target[0]][target[1]] = 9

# create a function that will act as the lazor path
# the function will check all squares in the path of the lazor


# inputs = grid, lazor list (a list of Lazor objects)
# outputs = lazor path in a list of positions
def lazor_movement(grid, Lazor_list):
    positions = []
    for lazor in Lazor_list:
        lp = lazor.position
        lazor_vector = lazor.vector
        grid[lp[0]][lp[1]] = 10
        start = lp
        positions.append(start)
        new_pos = start
        # go through the loop to create a list of lazor positions for each lazor
        while len(positions) > 0:
            # check positions in the lazor path in which the lazor will encounter a block
            x_check = (new_pos[0] + lazor_vector[0], new_pos[1])
            y_check = (new_pos[0], new_pos[1] + lazor_vector[1])
            # check to see if the lazor encounters a reflecting block
            if grid[x_check[0]][x_check[1]] == 3 or 6:
                lazor.reflect_x()
                new_pos = (new_pos[0] + lazor_vector[0], new_pos[1] + lazor_vector[1])
                positions.append(new_pos)
                continue
            elif grid[y_check[0]][y_check[1]] == 3 or 6:
                lazor.reflect_y()
                new_pos = (new_pos[0] + lazor_vector[0], new_pos[1] + lazor_vector[1])
                positions.append(new_pos)
                continue
            # check to see if the lazor encounters an opaque block
            elif grid[x_check[0]][x_check[1]] == 4 or 7:
                # in the x_check position, the lazor's last position is the x_check position
                lazor.absorb()
                new_pos = x_check
                positions.append(new_pos)
                # break loop since lazor is absorbed
                break
            elif grid[y_check[0]][y_check[1]] == 4 or 7:
                # in the y_check position, the lazor's last position is the y_check position
                lazor.absorb()
                new_pos = y_check
                positions.append(new_pos)
                # break loop since lazor is absorbed
                break
            # check to see if the lazor encounters a refracting block
            elif grid[x_check[0]][x_check[1]] == 5 or 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                lazor.refract_x()
                new_pos = (new_pos[0] + lazor_vector[0], new_pos[1] + lazor_vector[1])
                positions.append(new_pos)
                continue
            elif grid[y_check[0]][y_check[1]] == 5 or 8:
                # use lazor refract function to generate a new lazor
                # new lazor will be appended to list of Lazor objects
                lazor.refract_y()
                new_pos = (new_pos[0] + lazor_vector[0], new_pos[1] + lazor_vector[1])
                positions.append(new_pos)
                continue
            # continue for all other cases
            # break the loop when lazor reaches the end of the grid
            else:
                new_pos = (new_pos[0] + lazor_vector[0], new_pos[1] + lazor_vector[1])
                if new_pos[0] < 0 or new_pos[0] >= len(grid) or new_pos[1] < 0 or new_pos[1] >= len(grid[0]):
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

    def add_lazor(self, position, vector):
        self.position = position
        self.vector = vector
        return self.position, self.vector

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
        lazor_list.append(new_lazor)

    def absorb(self):
        self.vector[0] = 0
        self.vector[1] = 0

    def place_lazor(self, position, grid):
        self.position = position
        self.grid = grid
        grid[position[0]][position[1]] = 10


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