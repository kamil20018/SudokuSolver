from constants import *
from getboardnumbers import *
from itertools import *

#uber basic
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


def remove_candidates2(board):
    singles = get_n_valued_cells(board, 1)
    for single in singles:
        number = single[1][0]
        pos = single[0]
        for row in range(BOARD_SIZE):
            if row != pos[0] and number in board[row][pos[1]]:
                board[row][pos[1]].remove(number)
        for col in range(BOARD_SIZE):
            if col != pos[1] and number in board[pos[0]][col]:
                board[pos[0]][col].remove(number)
        box = get_numbers_box(pos)
        for row in range(box[0] * 3, (box[0] + 1) * 3):
            for col in range(box[1] * 3, (box[1] + 1) * 3):
                if [row, col] != pos and number in board[row][col]:
                    board[row][col].remove(number)


def hidden_single(board):
    # check for hidden single in a row
    for row in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = get_number_in_row(board, number, row, format = 1)
            if len(occurs_at) == 1 and len(board[row][occurs_at[0]]) > 1:
                board[row][occurs_at[0]] = [number]
                return True

    # check for hidden single in a column
    for col in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = get_number_in_column(board, number, col, format = 1)
            if len(occurs_at) == 1 and len(board[occurs_at[0]][col]) > 1:
                board[occurs_at[0]][col] = [number]
                return True

    # check for hidden single in a box
    for row_mult in range(3):
        for col_mult in range(3):
            for number in range(1, 10):
                occurs_at = get_number_in_box(board, number, row_mult, col_mult, format = 1)
                if len(occurs_at) == 1 and len(board[occurs_at[0][0]][occurs_at[0][1]]):
                    board[occurs_at[0][0]][occurs_at[0][1]] = [number]
                    return True


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


#all basic subset stuff
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


def naked_triple(board):
    #row
    for row in range(BOARD_SIZE):
        bi_cells = get_n_valued_cells_row(board, row, 2)
        tri_cells = get_n_valued_cells_row(board, row, 3)
        cells = bi_cells + tri_cells
        comb = list(combinations(cells, 3))
        for triple in comb:
            digits = set()
            columns = []
            for cell in triple:
                digits = digits | set(cell[1])
                columns.append(cell[0])
            digits = list(digits)
            if len(digits) == 3:
                for col in (x for x in range(BOARD_SIZE) if x not in columns):
                    for digit in digits:
                        if digit in board[row][col]:
                            board[row][col].remove(digit)
    #col
    for col in range(BOARD_SIZE):
        bi_cells = get_n_valued_cells_col(board, col, 2)
        tri_cells = get_n_valued_cells_col(board, col, 3)
        cells = bi_cells + tri_cells
        comb = list(combinations(cells, 3))
        for triple in comb:
            digits = set()
            rows = []
            for cell in triple:
                digits = digits | set(cell[1])
                rows.append(cell[0])
            digits = list(digits)
            if len(digits) == 3:
                for row in (x for x in range(BOARD_SIZE) if x not in rows):
                    for digit in digits:
                        if digit in board[row][col]:
                            board[row][col].remove(digit)
    #box
    for box_row in range(3):
        for box_col in range(3):
            bi_cells = get_n_valued_cells_box(board, box_row, box_col, 2)
            tri_cells = get_n_valued_cells_box(board, box_row, box_col, 3)
            cells = bi_cells + tri_cells
            if len(cells) < 3: break
            comb = list(combinations(cells, 3))
            for triple in comb:
                digits = set()
                points = []
                for cell in triple:
                    digits = digits | set(cell[1])
                    points.append(cell[0])
                digits = list(digits)
                if len(digits) == 3:
                    for row in range(3 * box_row, 3 * (box_row + 1)):
                        for col in range(3 * box_col, 3 * (box_col + 1)):
                            if [row, col] not in points:
                                for digit in digits:
                                    if digit in board[row][col]:
                                        board[row][col].remove(digit)


def naked_quad(board):
    #row
    for row in range(BOARD_SIZE):
        cells = []
        for x in range(2, 5):
            cells += get_n_valued_cells_row(board, row, x)
        comb = list(combinations(cells, 4))
        for quad in comb:
            digits = set()
            columns = []
            for cell in quad:
                digits = digits | set(cell[1])
                columns.append(cell[0])
            digits = list(digits)
            if len(digits) == 4:
                for col in (x for x in range(BOARD_SIZE) if x not in columns):
                    for digit in digits:
                        if digit in board[row][col]:
                            board[row][col].remove(digit)
    #col
    for col in range(BOARD_SIZE):
        cells = []
        for x in range(2, 5):
            cells += get_n_valued_cells_col(board, col, x)
        comb = list(combinations(cells, 4))
        for quad in comb:
            digits = set()
            rows = []
            for cell in quad:
                digits = digits | set(cell[1])
                rows.append(cell[0])
            digits = list(digits)
            if len(digits) == 4:
                for row in (x for x in range(BOARD_SIZE) if x not in rows):
                    for digit in digits:
                        if digit in board[row][col]:
                            board[row][col].remove(digit)
    #box
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for x in range(2, 5):
                cells += get_n_valued_cells_box(board, box_row, box_col, x)
            comb = list(combinations(cells, 4))
            for quad in comb:
                digits = set()
                points = []
                for cell in quad:
                    digits = digits | set(cell[1])
                    points.append(cell[0])
                digits = list(digits)
                if len(digits) == 4:
                    for row in range(3 * box_row, 3 * (box_row + 1)):
                        for col in range(3 * box_col, 3 * (box_col + 1)):
                            if [row, col] not in points:
                                for digit in digits:
                                    if digit in board[row][col]:
                                        board[row][col].remove(digit)


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


def hidden_triple(board):
    #row
    for row in range(BOARD_SIZE):
        sets = []
        for number in range(1, 10):
            positions = get_number_in_row(board, number, row, format = 1)
            if len(positions) >= 2 and len(positions) <= 3:
                sets.append([positions, number])
        combs = list(combinations(sets, 3))
        for triple in combs:
            cols = set()
            nums = []
            for elem in triple:
                cols = cols | set(elem[0])
                nums.append(elem[1])
            if len(cols) == 3:
                for col in cols:
                    for num in (x for x in range(1, 10) if x not in nums):
                        if num in board[row][col]:
                            board[row][col].remove(num)
    # col
    for col in range(BOARD_SIZE):
        sets = []
        for number in range(1, 10):
            positions = get_number_in_column(board, number, col, format = 1)
            if len(positions) >= 2 and len(positions) <= 3:
                sets.append([positions, number])
        combs = list(combinations(sets, 3))
        for triple in combs:
            rows = set()
            nums = []
            for elem in triple:
                rows = rows | set(elem[0])
                nums.append(elem[1])
            if len(rows) == 3:
                for row in rows:
                    for num in (x for x in range(1, 10) if x not in nums):
                        if num in board[row][col]:
                            board[row][col].remove(num)
                        
    # box
    for box_row in range(3):
        for box_col in range(3):
            sets = []
            for number in range(1, 10):
                positions = get_number_in_box(board, number, box_row, box_col, format = 2)
                if len(positions) >= 2 and len(positions) <= 3:
                    sets.append([positions, number])
            combs = list(combinations(sets, 3))
            for triple in combs:
                points = set()
                nums = []
                for elem in triple:
                    points = points | set(elem[0])
                    nums.append(elem[1])
                if len(points) == 3:
                    for point in points:
                        for num in (x for x in range(1, 10) if x not in nums):
                            if num in board[point[0]][point[1]]:
                                board[point[0]][point[1]].remove(num)


def hidden_quad(board):
    #row
    for row in range(BOARD_SIZE):
        sets = []
        for number in range(1, 10):
            positions = get_number_in_row(board, number, row, format = 1)
            if len(positions) >= 2 and len(positions) <= 4:
                sets.append([positions, number])
        combs = list(combinations(sets, 4))
        for quad in combs:
            cols = set()
            nums = []
            for elem in quad:
                cols = cols | set(elem[0])
                nums.append(elem[1])
            if len(cols) == 4:
                for col in cols:
                    for num in (x for x in range(1, 10) if x not in nums):
                        if num in board[row][col]:
                            board[row][col].remove(num)
    # col
    for col in range(BOARD_SIZE):
        sets = []
        for number in range(1, 10):
            positions = get_number_in_column(board, number, col, format = 1)
            if len(positions) >= 2 and len(positions) <= 4:
                sets.append([positions, number])
        combs = list(combinations(sets, 4))
        for quad in combs:
            rows = set()
            nums = []
            for elem in quad:
                rows = rows | set(elem[0])
                nums.append(elem[1])
            if len(rows) == 4:
                for row in rows:
                    for num in (x for x in range(1, 10) if x not in nums):
                        if num in board[row][col]:
                            board[row][col].remove(num)
    # box
    for box_row in range(3):
        for box_col in range(3):
            sets = []
            for number in range(1, 10):
                positions = get_number_in_box(board, number, box_row, box_col, format = 2)
                if len(positions) >= 2 and len(positions) <= 4:
                    sets.append([positions, number])
            combs = list(combinations(sets, 4))
            for quad in combs:
                points = set()
                nums = []
                for elem in quad:
                    points = points | set(elem[0])
                    nums.append(elem[1])
                if len(points) == 4:
                    for point in points:
                        for num in (x for x in range(1, 10) if x not in nums):
                            if num in board[point[0]][point[1]]:
                                board[point[0]][point[1]].remove(num)

#miscellaneus
def x_wing(board):
    #vertical elimination
    for row in range(BOARD_SIZE - 1):
        for number in range(10):
            occurs_at = get_number_in_row(board, number, row, format = 1)
            if len(occurs_at) == 2:  #if 2 numbers in row
                for y in range(row + 1, BOARD_SIZE): #y iterates below the row with 2 numbers
                    if occurs_at == get_number_in_row(board, number, y, format = 1):
                        for row_del in range(BOARD_SIZE):
                            if row_del not in {row, y}:
                                if number in board[row_del][occurs_at[0]]:
                                    board[row_del][occurs_at[0]].remove(number)
                                if number in board[row_del][occurs_at[1]]:
                                    board[row_del][occurs_at[1]].remove(number)
    #horizontal elimination
    for col in range(BOARD_SIZE - 1):
        for number in range(10):
            occurs_at = get_number_in_column(board, number, col, format = 1)
            if len(occurs_at) == 2:  #if 2 numbers in col
                for y in range(col + 1, BOARD_SIZE): #y iterates below the row with 2 numbers
                    if occurs_at == get_number_in_column(board, number, y, format = 1):
                        for col_del in range(BOARD_SIZE):
                            if col_del not in {col, y}:
                                if number in board[occurs_at[0]][col_del]:
                                    board[occurs_at[0]][col_del].remove(number)
                                if number in board[occurs_at[1]][col_del]:
                                    board[occurs_at[1]][col_del].remove(number)
    return True


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


def kite(board):
    for number in range(BOARD_SIZE):
        for row in range(BOARD_SIZE):
            occurs_at_1 = get_number_in_row(board, number, row, format = 1)
            if len(occurs_at_1) == 2 and occurs_at_1[0] // 3 != occurs_at_1[1] // 3:
                occurs_at_2 = []
                for col in range(3 * (occurs_at_1[0] // 3), 3 * (occurs_at_1[0] // 3 + 1)): #cols in 1st nums box
                    if col != occurs_at_1[0]:
                        occurs_at_2 = get_number_in_column(board, number, col, format = 1)
                        if len(occurs_at_2) == 2 and occurs_at_2[0] // 3 != occurs_at_2[1] // 3:
                            row_del = -1
                            if occurs_at_2[0] // 3 == row // 3:
                                row_del = occurs_at_2[1]
                            elif occurs_at_2[1] // 3 == row // 3:
                                row_del = occurs_at_2[0]
                            col_del = occurs_at_1[1]
                            if row_del > 1 and number in board[row_del][col_del]:
                                board[row_del][col_del].remove(number)
                occurs_at_2 = []
                for col in range(3 * (occurs_at_1[1] // 3), 3 * (occurs_at_1[1] // 3 + 1)): #cols in 1st nums box
                    if col != occurs_at_1[1]:
                        occurs_at_2 = get_number_in_column(board, number, col, format = 1)
                        if len(occurs_at_2) == 2 and occurs_at_2[0] // 3 != occurs_at_2[1] // 3:
                            row_del = -1
                            if occurs_at_2[0] // 3 == row // 3:
                                row_del = occurs_at_2[1]
                            elif occurs_at_2[1] // 3 == row // 3:
                                row_del = occurs_at_2[0]
                            col_del = occurs_at_1[0]
                            if row_del > 1 and number in board[row_del][col_del]:
                                board[row_del][col_del].remove(number)
                            
                            