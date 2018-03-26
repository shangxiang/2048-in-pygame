from random import randrange, choice

def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

field = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


def spawn(field):
    new_element = 4 if randrange(100) > 89 else 2
    (i, j) = choice([(i, j) for i in range(4) for j in range(4) if field[i][j] == 0])
    field[i][j] = new_element
    return field

def move_is_possible(field, direction):
    def row_is_left_movable(row):
        def change(i):
            if row[i] == 0 and row[i + 1] != row[i]:
                return True
            if row[i] != 0 and row[i + 1] == row[i]:
                return True
            return False

        return any(change(i) for i in range(len(row) - 1))

    check = {}
    check['left'] = lambda field: any(row_is_left_movable(row) for row in field)
    check['right'] = lambda field: check['left'](invert(field))
    check['up'] = lambda field: check['left'](transpose(field))
    check['down'] = lambda field: check['right'](transpose(field))

    if direction in check:
        return check[direction](field)
    else:
        return False

def move_row_left(row):
    def tighten(row):
        new_row = [i for i in row if i != 0]
        new_row += [0 for i in range(len(row) - len(new_row))]
        return new_row

    def merge(row):
        pair = False
        new_row = []
        for i in range(len(row)):
            if pair:
                new_row.append(2 * row[i])
                #self.score += 2 * row[i]
                pair = False
            else:
                if i + 1 < len(row) and row[i] == row[i + 1]:
                    pair = True
                    new_row.append(0)
                else:
                    new_row.append(row[i])
        assert len(new_row) == len(row)
        return new_row

    return tighten(merge(tighten(row)))

def move_left(field, direction='left'):
    if move_is_possible(field, direction):
        return [move_row_left(row) for row in field]
    else:
        return field

def move_right(field, direction = 'right'):
    return [invert(move_left(invert(field),direction))]

def move_up(field):
    return [transpose(move_left(transpose(field),'up'))]

def move_down(field):
    return [transpose(move_right(transpose(field),'down'))]