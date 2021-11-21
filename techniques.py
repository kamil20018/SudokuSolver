from constants import *

#basic candidate removal using sudoku rules
def remove_candidates(board):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if len(board[row][column]) != 1:
                candidates = board[row][column].copy()
                for index in range(BOARD_SIZE):
                    #remove candidates using row
                    if len(board[row][index]) == 1:
                        try:
                            candidates.remove(board[row][index][0])
                        except ValueError:
                            pass
                    #remove candidates column
                    if len(board[index][column]) == 1:
                        try:
                            candidates.remove(board[index][column][0])
                        except ValueError:
                            pass
                board[row][column] = candidates.copy()
                
    #remove candidates from box
    for row_mult in range(3):
        for col_mult in range(3):
            for row in range(3):
                for column in range(3):
                    if len(board[row + 3 * row_mult][column + 3 * col_mult]) == 1:
                        for act_row in range(3 * row_mult, 3 * (row_mult + 1)):
                            for act_column in range(3 * col_mult, 3 * (col_mult + 1)):
                                if len(board[act_row][act_column]) != 1:
                                    try:
                                        board[act_row][act_column].remove(board[row + 3 * row_mult][column + 3 * col_mult][0])
                                    except ValueError:
                                        pass

#updates the other candidates in case a digit was placed
def update_candidates(board, given_row, given_column, number):
    for row in range(BOARD_SIZE):
        try:
            if row != given_row:
                board[row][given_column].remove(number)
        except ValueError:
            pass
    for column in range(BOARD_SIZE):
        try:
            if column != given_column:
                board[given_row][column].remove(number)
        except ValueError:
            pass

    box_row = given_row // 3
    box_column = given_column // 3

    for row in range(box_row * 3, (box_row + 1) * 3):
        for column in range(box_column * 3, (box_column + 1) * 3):
            try:
                if row != given_row and column != given_column:
                    board[row][column].remove(number)
            except ValueError:
                pass

#searches for hidden singles
def hidden_single(board):
    #check for hidden single in a row
    for row in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = []
            for column in range(BOARD_SIZE):
                if number in board[row][column]:       
                    occurs_at.append(column)
            if len(occurs_at) == 1:
                board[row][occurs_at[0]] = [number]
                update_candidates(board, row, occurs_at[0], number)

    #check for hidden single in a column
    for column in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = []
            for row in range(BOARD_SIZE):
                if number in board[row][column]:       
                    occurs_at.append(row)
            if len(occurs_at) == 1:
                board[occurs_at[0]][column] = [number]
                update_candidates(board, occurs_at[0], column, number)     

    #check for hidden single in a box   
    for row_mult in range(3):
        for col_mult in range(3):
            for number in range(1, 10):
                occurs_at = []
                for row in range(row_mult * 3, (row_mult + 1) * 3):
                    for column in range(col_mult * 3, (col_mult + 1) * 3):  
                        if number in board[row][column]:       
                            occurs_at.append([row, column])
                if len(occurs_at) == 1:
                    board[occurs_at[0][0]][occurs_at[0][1]] = [number]
                    update_candidates(board, occurs_at[0][0], occurs_at[0][1], number)
    
def locked_candidates_pointing(board):
    for row_mult in range(3):
        for col_mult in range(3):
            for number in range(1, 10):
                occurs_at = []
                for row in range(row_mult * 3, (row_mult + 1) * 3):
                    for column in range(col_mult * 3, (col_mult + 1) * 3):
                        if number in board[row][column] or board[row][column] == [number]:   
                            occurs_at.append([row, column])
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
                                        board[pos_row][box_col * 3 + col_del].remove(number)
                                    except ValueError:
                                            pass
                    if same_col:
                        for box_row in range(3):
                            if box_row != row_mult:
                                for row_del in range(3):
                                    try:
                                        board[box_row * 3 + row_del][pos_col].remove(number)
                                    except ValueError:
                                            pass

def locked_candidates_claiming(board):
    for row in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = []
            for column in range(BOARD_SIZE):
                if number in board[row][column]:
                    occurs_at.append(column)
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
    
    for column in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = []
            for row in range(BOARD_SIZE):
                if number in board[row][column]:
                    occurs_at.append(row)
            if len(occurs_at) >= 2 and len(occurs_at) <= 3:
                same_box = True
                row_pos = occurs_at[0]
                for pos in occurs_at:
                    if(pos // 3 != row_pos // 3):
                        same_box = False
                        break
                if same_box:
                    for box_col in range(3 * (column // 3), 3 * (column // 3 + 1)):
                        for box_row in range(3 * (row_pos // 3), 3 * (row_pos // 3 + 1)):
                            if box_col != column:
                                try:
                                    board[box_row][box_col].remove(number)
                                except ValueError:
                                    pass

def naked_pair(board):
    #box
    for row_mult in range(3):
        for col_mult in range(3):
            pairs = []
            for row in range(row_mult * 3, (row_mult + 1) * 3):
                for column in range(col_mult * 3, (col_mult + 1) * 3):  
                    if len(board[row][column]) == 2:
                        pairs.append([board[row][column], [row, column]]) #stores a pair of numbers and their position
            for x in range(len(pairs)):
                for y in range(len(pairs)):
                    if x != y and pairs[x][0] == pairs[y][0]:
                        first_removable = pairs[x][0][0]
                        second_removable = pairs[x][0][1]
                        for row in range(row_mult * 3, (row_mult + 1) * 3):
                            for column in range(col_mult * 3, (col_mult + 1) * 3): 
                                if [row, column] not in [pairs[x][1], pairs[y][1]]:
                                    try:
                                        board[row][column].remove(first_removable)
                                    except ValueError:
                                            pass
                                    try:
                                        board[row][column].remove(second_removable)
                                    except ValueError:
                                            pass

    #row
    for row in range(BOARD_SIZE):
        pairs = []
        for column in range(BOARD_SIZE):
            if len(board[row][column]) == 2:
                pairs.append([board[row][column], [row, column]])
        for x in range(len(pairs)):
            for y in range(len(pairs)):
                if x != y and pairs[x][0] == pairs[y][0]:
                    first_removable = pairs[x][0][0]
                    second_removable = pairs[x][0][1]
                    for col in range(BOARD_SIZE):
                        if col != pairs[x][1][1] and col != pairs[y][1][1]:
                            try:
                                board[row][col].remove(second_removable)
                            except ValueError:
                                pass

                            try:
                                board[row][col].remove(first_removable)
                            except ValueError:
                                pass
                      
    #column
    for column in range(BOARD_SIZE):
        pairs = []
        for row in range(BOARD_SIZE):
            if len(board[row][column]) == 2:
                pairs.append([board[row][column], [row, column]])
        for x in range(len(pairs)):
            for y in range(len(pairs)):
                if x != y and pairs[x][0] == pairs[y][0]:
                    first_removable = pairs[x][0][0]
                    second_removable = pairs[x][0][1]
                    for new_row in range(BOARD_SIZE):
                        if new_row != pairs[x][1][0] and new_row != pairs[y][1][0]:
                            try:
                                board[new_row][column].remove(first_removable)
                            except ValueError:
                                pass
                            try:
                                board[new_row][column].remove(second_removable)
                            except ValueError:
                                pass
                            