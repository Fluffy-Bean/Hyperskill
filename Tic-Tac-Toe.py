def check_goes(field):
    """
    Check how many goes each player had
    """
    x, o = 0, 0

    for row in field:
        for col in row:
            if col == 'X':
                x += 1
            elif col == 'O':
                o += 1

    return x, o

def check_rows(field):
    """
    Check for horizontals
    """
    x, o = False, False

    for row in field:
        if row[0] == row[1] == row[2]:
            # Now we just need to check the first value
            if row[0] == 'X':
                x = True
            elif row[0] == 'O':
                o = True

    return x, o

def check_cols(field):
    """
    Check for verticals
    """
    x, o = False, False

    for column in range(3):
        if field[0][column] == field[1][column] == field[2][column]:
            if field[0][column] == 'X':
                x = True
            elif field[0][column] == 'O':
                o = True

    return x, o

def check_digs(field):
    """
    Check for diagonals
    """
    x, o = False, False

    # Check both angles
    if field[0][0] == field[2][2] == field[1][1]:
        if field[1][1] == 'X':
            x = True
        elif field[1][1] == 'O':
            o = True
        else:
            return False, False
    elif field[0][2] == field[2][0] == field[1][1]:
        if field[1][1] == 'X':
            x = True
        elif field[1][1] == 'O':
            o = True
        else:
            return False, False

    return x, o

def check_cell(field, coords, val='X'):
    """
    Set value on playing field
    False = User needs to try again
    """
    coords = coords.split(" ")
    if len(coords) == 2:
        try:
            # Human correction
            cord_x = int(coords[0]) - 1
            cord_y = int(coords[1]) - 1
        except TypeError:
            # Cheap way to check if the input is a number lol
            print("You should enter numbers!")
            return False
    else:
        print("You should enter numbers!")
        return False

    # smelly human correction
    if not 0 <= cord_x <= 2:
        print("Coordinates should be from 1 to 3!")
        return False
    if not 0 <= cord_y <= 2:
        print("Coordinates should be from 1 to 3!")
        return False

    if field[cord_x][cord_y] == "_":
        field[cord_x][cord_y] = val
        return field
    else:
        print("This cell is occupied! Choose another one!")
        print(field[cord_y][cord_x])
        return False


if __name__ == '__main__':
    # Get input from user
    # stage = input()
    # field = [
    #     [stage[0], stage[1], stage[2]],
    #     [stage[3], stage[4], stage[5]],
    #     [stage[6], stage[7], stage[8]],
    # ]

    field = [
        ['_', '_', '_'],
        ['_', '_', '_'],
        ['_', '_', '_'],
    ]

    # Set values
    x_win, o_win = False, False
    x_goes, o_goes = 0, 0
    game_active = True
    current_go = 'X'
    go_finished = False

    # Print stage
    print('----------')
    for col in field:
        print('|', col[0], col[1], col[2], '|')
    print('----------')

    while game_active:
        while not go_finished:
            cords = input()
            n = check_cell(field, cords, current_go)

            if n:
                field = n
                go_finished = True

        print('----------')
        for col in field:
            print('|', col[0], col[1], col[2], '|')
        print('----------')

        j, k = check_rows(field)
        if j:
            x_win = True
        if k:
            o_win = True

        j, k = check_cols(field)
        if j:
            x_win = True
        if k:
            o_win = True

        j, k = check_digs(field)
        if j:
            x_win = True
        if k:
            o_win = True

        x_goes, o_goes = check_goes(field)

        if x_win and o_win:
            print('Impossible')
        elif max(x_goes, o_goes) - min(x_goes, o_goes) > 1:
            print('Impossible')
        elif x_win and not o_win:
            print('X wins')
            game_active = False
        elif not x_win and o_win:
            print('O wins')
            game_active = False
        elif not x_win and not o_win and (x_goes + o_goes == 9):
            print('Draw')
            game_active = False

        if current_go == 'X':
            current_go = 'O'
        else:
            current_go = 'X'

        go_finished = False
