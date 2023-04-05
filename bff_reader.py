'''
Author: Braden Barlean
'''
def read_bff(file_name):
    '''
    This function serves to open a .bff file provided with the
    Lazor Project, collects the data from the file, and stores the
    information in a dictionary. 
    
    Input: file_name
    Output: data dictionary
    '''
    with open(file_name, 'r') as f:

        blocks = {'a': [], 'b': [], 'c': []}
        lazers = []
        points = []

        data = {}

        for line in f:
            # Skip line if it is a comment
            if line.startswith('#'):
                continue
            # Remove leading/trailing whitespaces
            line = line.strip()
            # Skip the line if it is empty
            if not line:
                continue
            # Begin the grid list when the line has 'GRID START'
            if line.startswith('GRID START'):
                grid = []
                continue
            # Save the grid list to the 'grid' key in the data
            # dictionary when the line has 'GRID END'
            if line.startswith('GRID STOP'):
                data['grid'] = grid
                continue

            # Replace 3 spaces with 1 space before processing
            # the line
            line = line.replace('   ', ' ')

            # Split the line to analyze the first letter
            parts = line.strip().split()
            if parts[0] == 'A':
                blocks['a'].append(int(parts[1]))
            elif parts[0] == 'B':
                blocks['b'].append(int(parts[1]))
            elif parts[0] == 'C':
                blocks['c'].append(int(parts[1]))
            elif parts[0] == 'L':
                lazers.append((int(parts[1]), int(parts[2]),
                               int(parts[3]), int(parts[4])))
            elif parts[0] == 'P':
                points.append((int(parts[1]), int(parts[2])))
            else:
                grid.append(list(line))

        # Add spaces before and after the first and last elements
        # of each line
        for ele in grid:
            ele.insert(0, ' ')
            ele.append(' ')

        # Add a row of spaces between each line of the grid
        for i in range(0,len(grid)+len(grid),2):
            empty_row = [' '] * len(grid[i])
            grid.insert(i, empty_row)

        # Add a row of spaces at the end of the grid
        grid.append(empty_row)

        data = {'grid': grid, 'blocks': blocks, 'lazers': lazers,
                'points': points}
    return data

if __name__ == '__main__':
    print(read_bff('mad_1.bff'))
