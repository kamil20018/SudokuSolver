from constants import *

# basic candidate removal using sudoku rules

def get_number_in_row(board, number, row, format):
    occurs_at = []
    for col in range(BOARD_SIZE):
        if number in board[row][col]:
            match format:
                case 1:
                    occurs_at.append(col)
    return occurs_at


def get_number_in_column(board, number, col, format):
    occurs_at = []
    for row in range(BOARD_SIZE):
        if number in board[row][col]:
            match format:
                case 1:
                    occurs_at.append(row)
    return occurs_at


def get_number_in_box(board, number, row_mult, col_mult, format):
    occurs_at = []
    for row in range(row_mult * 3, (row_mult + 1) * 3):
        for col in range(col_mult * 3, (col_mult + 1) * 3):
            if number in board[row][col]:
                match format:
                    case 1:
                        occurs_at.append([row, col]) 
    return occurs_at


def get_n_valued_cells(board, n):
    cells = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if len(board[row][col]) == n:
                cells.append([[row, col], board[row][col]])
    return cells


def remove_candidates(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if len(board[row][col]) != 1:
                candidates = board[row][col].copy()
                for index in range(BOARD_SIZE):
                    to_del = board[row][index][0]
                    if len(board[row][index]) == 1 and to_del in candidates:
                        candidates.remove(to_del)
                    to_del = board[index][col][0]
                    if len(board[index][col]) == 1 and to_del in candidates:
                        candidates.remove(board[index][col][0])
                board[row][col] = candidates.copy()

    # remove candidates from box
    for row_mult in range(3):
        for col_mult in range(3):
            for row in range(3 * row_mult, 3 * (row_mult + 1)):
                for col in range(3 * col_mult, 3 * (col_mult + 1)):
                    if len(board[row][col]) == 1:
                        for act_row in range(3 * row_mult, 3 * (row_mult + 1)):
                            for act_col in range(3 * col_mult, 3 * (col_mult + 1)):
                                to_del = board[row][col][0]
                                if len(board[act_row][act_col]) != 1 and to_del in board[act_row][act_col]:
                                    board[act_row][act_col].remove(to_del)


#useless
def update_candidates(board, given_row, given_col, number):
    for row in range(BOARD_SIZE):
        if row != given_row and number in board[row][given_col]:
            board[row][given_col].remove(number)

    for col in range(BOARD_SIZE):
        if col != given_col and number in board[given_row][col]:
            board[given_row][col].remove(number)

    box_row = given_row // 3
    box_col = given_col // 3

    for row in range(box_row * 3, (box_row + 1) * 3):
        for col in range(box_col * 3, (box_col + 1) * 3):
            if row != given_row and col != given_col and number in board[row][col]:
                board[row][col].remove(number)


def hidden_single(board):
    # check for hidden single in a row
    for row in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = get_number_in_row(board, number, row, format = 1)
            if len(occurs_at) == 1:
                board[row][occurs_at[0]] = [number]

    # check for hidden single in a column
    for col in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = get_number_in_column(board, number, col, format = 1)
            if len(occurs_at) == 1:
                board[occurs_at[0]][col] = [number]

    # check for hidden single in a box
    for row_mult in range(3):
        for col_mult in range(3):
            for number in range(1, 10):
                occurs_at = get_number_in_box(board, number, row_mult, col_mult, format = 1)
                if len(occurs_at) == 1:
                    board[occurs_at[0][0]][occurs_at[0][1]] = [number]


def locked_candidates_pointing(board):
    for row_mult in range(3):
        for col_mult in range(3):
            for number in range(1, 10):
                occurs_at = get_number_in_box(board, number, row_mult, col_mult, format = 1)
                if len(occurs_at) >= 2 and len(occurs_at) <= 3:
                    pos_row = occurs_at[0][0]
                    same_row = True
                    pos_col = occurs_at[0][1]
                    same_col = True
                    for pos in occurs_at:
                        if(pos_row != pos[0]):
                            same_row = False
                        if(pos_col != pos[1]):
                            same_col = False
                    if same_row:
                        for box_col in range(3):
                            if box_col != col_mult:
                                for col_del in range(3):
                                    try:
                                        board[pos_row][box_col * 3 +
                                                       col_del].remove(number)
                                    except ValueError:
                                        pass
                    if same_col:
                        for box_row in range(3):
                            if box_row != row_mult:
                                for row_del in range(3):
                                    try:
                                        board[box_row * 3 +
                                              row_del][pos_col].remove(number)
                                    except ValueError:
                                        pass


def locked_candidates_claiming(board):
    for row in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = get_number_in_row(board, number, row, format = 1)
            if len(occurs_at) >= 2 and len(occurs_at) <= 3:
                same_box = True
                col_pos = occurs_at[0]
                for pos in occurs_at:
                    if(pos // 3 != col_pos // 3):
                        same_box = False
                        break
                if same_box:
                    for box_row in range(3 * (row // 3), 3 * (row // 3 + 1)):
                        for box_col in range(3 * (col_pos // 3), 3 * (col_pos // 3 + 1)):
                            if box_row != row:
                                try:
                                    board[box_row][box_col].remove(number)
                                except ValueError:
                                    pass

    for col in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = get_number_in_column(board, number, col, format = 1)
            if len(occurs_at) >= 2 and len(occurs_at) <= 3:
                same_box = True
                row_pos = occurs_at[0]
                for pos in occurs_at:
                    if(pos // 3 != row_pos // 3):
                        same_box = False
                        break
                if same_box:
                    for box_col in range(3 * (col // 3), 3 * (col // 3 + 1)):
                        for box_row in range(3 * (row_pos // 3), 3 * (row_pos // 3 + 1)):
                            if box_col != col:
                                try:
                                    board[box_row][box_col].remove(number)
                                except ValueError:
                                    pass


def naked_pair(board):
    # box
    for row_mult in range(3):
        for col_mult in range(3):
            pairs = []
            for row in range(row_mult * 3, (row_mult + 1) * 3):
                for col in range(col_mult * 3, (col_mult + 1) * 3):
                    if len(board[row][col]) == 2:
                        # stores a pair of numbers and their position
                        pairs.append([board[row][col], [row, col]])
            for x in range(len(pairs)):
                for y in range(len(pairs)):
                    if x != y and pairs[x][0] == pairs[y][0]:
                        first_rem = pairs[x][0][0]
                        second_rem = pairs[x][0][1]
                        for row in range(row_mult * 3, (row_mult + 1) * 3):
                            for col in range(col_mult * 3, (col_mult + 1) * 3):
                                if [row, col] not in [pairs[x][1], pairs[y][1]]:
                                    if first_rem in board[row][col]:
                                        board[row][col].remove(first_rem)
                                    if second_rem in board[row][col]:
                                        board[row][col].remove(second_rem)

    # row
    for row in range(BOARD_SIZE):
        pairs = []
        for col in range(BOARD_SIZE):
            if len(board[row][col]) == 2:
                pairs.append([board[row][col], [row, col]])
        for x in range(len(pairs)):
            for y in range(len(pairs)):
                if x != y and pairs[x][0] == pairs[y][0]:
                    first_rem = pairs[x][0][0]
                    second_rem = pairs[x][0][1]
                    for col in range(BOARD_SIZE):
                        if col != pairs[x][1][1] and col != pairs[y][1][1]:
                            if second_rem in board[row][col]:
                                board[row][col].remove(second_rem)
                            if first_rem in board[row][col]:
                                board[row][col].remove(first_rem)

    # column
    for col in range(BOARD_SIZE):
        pairs = []
        for row in range(BOARD_SIZE):
            if len(board[row][col]) == 2:
                pairs.append([board[row][col], [row, col]])
        for x in range(len(pairs)):
            for y in range(len(pairs)):
                if x != y and pairs[x][0] == pairs[y][0]:
                    first_rem = pairs[x][0][0]
                    second_rem = pairs[x][0][1]
                    for new_row in range(BOARD_SIZE):
                        if new_row != pairs[x][1][0] and new_row != pairs[y][1][0]:
                            if first_rem in board[new_row][col]:
                                board[new_row][col].remove(first_rem)
                            if second_rem in board[new_row][col]:
                                board[new_row][col].remove(second_rem)


def hidden_pair(board):
    # box
    def handle_pairs(pairs):
        if len(pairs) > 1:
            for x in range(len(pairs)):
                for y in range(x):
                    s1 = {pairs[x][0][0], pairs[x][1][0]}
                    s2 = {pairs[y][0][0], pairs[y][1][0]}
                    if x != y and s1 == s2:
                        notRemovable = [pairs[x][0][1], pairs[y][0][1]]
                        for number in range(1, 10):
                            if number not in notRemovable:
                                for pos in s1:
                                    try:
                                        board[pos[0]][pos[1]].remove(
                                            number)
                                    except ValueError:
                                        pass
    for row_mult in range(3):
        for col_mult in range(3):
            pairs = []
            for number in range(1, 10):
                occursAt = []
                for row in range(row_mult * 3, (row_mult + 1) * 3):
                    for col in range(col_mult * 3, (col_mult + 1) * 3):
                        if number in board[row][col]:
                            occursAt.append([(row, col), number])
                if len(occursAt) == 2:
                    pairs.append(occursAt.copy())
            handle_pairs(pairs)

    # row
    for row in range(BOARD_SIZE):
        pairs = []
        for number in range(1, 10):
            occursAt = []
            for col in range(BOARD_SIZE):
                if number in board[row][col]:
                        occursAt.append([(row, col), number])
            if len(occursAt) == 2:
                    pairs.append(occursAt.copy())
        handle_pairs(pairs)

    # column
    for col in range(BOARD_SIZE):
        pairs = []
        for number in range(1, 10):
            occursAt = []
            for row in range(BOARD_SIZE):
                if number in board[row][col]:
                        occursAt.append([(row, col), number])
            if len(occursAt) == 2:
                    pairs.append(occursAt.copy())
        handle_pairs(pairs)


def x_wing(board):
    #vertical elimination
    for row in range(BOARD_SIZE - 1):
        for number in range(10):
            occurs_at = get_number_in_row(board, number, row, format = 1)
            if len(occurs_at) == 2:  #if 2 numbers in row
                for y in range(row + 1, BOARD_SIZE): #y iterates below the row with 2 numbers
                    correct = True
                    if number in board[y][occurs_at[0]] and number in board[y][occurs_at[1]]:
                        for cell in range(BOARD_SIZE):
                            if cell not in occurs_at and number in board[y][cell]:
                                correct = False
                        if correct:
                            #elim number from columns: occurs_at       not elim from rows: row and y, 
                            for cell in range(BOARD_SIZE):
                                if cell not in [row, y]:
                                    if number in board[cell][occurs_at[0]]:
                                        board[cell][occurs_at[0]].remove(number)
                                    if number in board[cell][occurs_at[1]]:
                                        board[cell][occurs_at[1]].remove(number)
                    if correct: 
                        break
    #horizontal elimination
    for col in range(BOARD_SIZE - 1):
        for number in range(10):
            occurs_at = get_number_in_column(board, number, col, format = 1)
            if len(occurs_at) == 2:  #if 2 numbers in column
                for x in range(col + 1, BOARD_SIZE): #x iterates below the row with 2 numbers
                    correct = True
                    if number in board[occurs_at[0]][x] and number in board[occurs_at[1]][x]:
                        for cell in range(BOARD_SIZE):
                            if cell not in occurs_at and number in board[cell][x]:
                                correct = False
                        if correct:
                            #elim number from columns: occurs_at       not elim from rows: row and x, 
                            for cell in range(BOARD_SIZE):
                                if cell not in [col, x]:
                                    if number in board[occurs_at[0]][cell]:
                                        board[occurs_at[0]][cell].remove(number)
                                    if number in board[occurs_at[1]][cell]:
                                        board[occurs_at[1]][cell].remove(number)
                    if correct: 
                        break


def skyscraper(board):
    #horizontal
    for number in range(1, 10):
        for row_1 in range(BOARD_SIZE - 1):
            occurs_at_1 = get_number_in_row(board, number, row_1, format = 1)
            if len(occurs_at_1) == 2:
                for row_2 in range(row_1 + 1, BOARD_SIZE):
                    occurs_at_2 = get_number_in_row(board, number, row_2, format = 1)
                    if len(occurs_at_2) == 2 and len(set(occurs_at_1) | set(occurs_at_2)) == 3:
                        base = (set(occurs_at_1) & set(occurs_at_2)).pop()
                        col_1 = [x for x in occurs_at_1 if x != base][0]
                        col_2 = [x for x in occurs_at_2 if x != base][0]
                        box_1 = [row_1 // 3, col_1 // 3]
                        box_2 = [row_2 // 3, col_2 // 3]
                        if box_1[0] != box_2[0] and box_1[1] == box_2[1] and col_1 != col_2:
                            for row in range((3 * box_1[0]), 3 * (box_1[0] + 1)):
                                if number in board[row][col_2]:
                                    board[row][col_2].remove(number)
                            for row in range((3 * box_2[0]), 3 * (box_2[0] + 1)):
                                if number in board[row][col_1]:
                                    board[row][col_1].remove(number)
    #vertical
    for number in range(1, 10):
        for col_1 in range(BOARD_SIZE - 1):
            occurs_at_1 = get_number_in_column(board, number, col_1, format = 1)
            if len(occurs_at_1) == 2:
                for col_2 in range(col_1 + 1, BOARD_SIZE):
                    occurs_at_2 = get_number_in_column(board, number, col_2, format = 1)
                    if len(occurs_at_2) == 2 and len(set(occurs_at_1) | set(occurs_at_2)) == 3:
                        base = (set(occurs_at_1) & set(occurs_at_2)).pop()
                        row_1 = [x for x in occurs_at_1 if x != base][0]
                        row_2 = [x for x in occurs_at_2 if x != base][0]
                        box_1 = [row_1 // 3, col_1 // 3]
                        box_2 = [row_2 // 3, col_2 // 3]
                        if box_1[0] == box_2[0] and box_1[1] != box_2[1] and row_1 != row_2:
                            for col in range((3 * box_1[1]), 3 * (box_1[1] + 1)):
                                if number in board[row_2][col]:
                                    board[row_2][col].remove(number)
                            for col in range((3 * box_2[1]), 3 * (box_2[1] + 1)):
                                if number in board[row_1][col]:
                                    board[row_1][col].remove(number)