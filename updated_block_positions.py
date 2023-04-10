'''
This is a revised block positions function that can generate all the
possible block positions for a given grid and block list.
The function returns a list of lists, where each list contains touples 
of block positions.

The order in which the blocks are brought in are preserved as the order
of the positions in the returned list.
'''

import itertools

def block_positions(grid, block_list):
    # create a list of available positions on the grid
    available_positions = []
    for row_idx, row in enumerate(grid):
        for col_idx, cell in enumerate(row):
            if cell == 2:
                available_positions.append((row_idx, col_idx))

    # create a dictionary of block types and their counts
    block_counts = {}
    for block_type in block_list:
        block_counts[block_type] = block_counts.get(block_type, 0) + 1

    # create a list of positions for each block type separately
    block_positions = []
    for block_type, count in block_counts.items():
        positions = list(itertools.combinations(available_positions, count))
        for position_set in positions:
            for position in position_set:
                block_positions.append(position)

    # combine positions for each block type to form all valid block positions
    valid_positions = []
    for i in range(0, len(block_positions), len(block_list)):
        valid_positions.append(block_positions[i:i+len(block_list)])

    return valid_positions
