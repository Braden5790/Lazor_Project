filename = "mad_1.bff"
data = {}

with open(filename) as f:
    for line in f:
        if line.startswith('#'):
            continue
        line = line.strip()
        if not line:
            continue
        if line.startswith('GRID START'):
            grid = []
            continue
        if line.startswith('GRID STOP'):
            data['grid'] = grid
            continue
        parts = line.split()
        if parts[0] == 'A':
            data['A'] = int(parts[1])
        elif parts[0] == 'B':
            data['B'] = int(parts[1])
        elif parts[0] == 'C':
            data['C'] = int(parts[1])
        elif parts[0] == 'L':
            # data['lazers'] = []
            my_list = []
            # print(parts[1])
            for i in range(int(parts[1])):
                x = parts[1]
                y = parts[2]
                vx = parts[3]
                vy =  parts[4]
                my_list.append({'x': x, 'y': y, 'vx': vx, 'vy': vy})
                # print(f'{x} {y} {vx} {vy}')
            data['lazers'] = my_list
        elif parts[0] == 'P':
            # data['points'] = []
            # print(parts)
            new_list = []
            for i in range(int(parts[1])):
                x = parts[1]
                y = parts[2]
                new_list.append({'x': x, 'y': y})
                # print(x,y)
            data['points'] = new_list
        else:
            grid.append(list(line))

print(data)
