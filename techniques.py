from constants import *

#basic candidate removal using sudoku rules
def remove_candidates(board):
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            if(len(board[row][column]) != 1):
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
                    if(len(board[row + 3 * row_mult][column + 3 * col_mult]) == 1):
                        for act_row in range(3 * row_mult, 3 * (row_mult + 1)):
                            for act_column in range(3 * col_mult, 3 * (col_mult + 1)):
                                if(len(board[act_row][act_column]) != 1):
                                    try:
                                        board[act_row][act_column].remove(board[row + 3 * row_mult][column + 3 * col_mult][0])
                                    except ValueError:
                                        pass

#updates the other candidates in case a digit was placed
def update_candidates(board, given_row, given_column, number):
    for row in range(BOARD_SIZE):
        try:
            if(row != given_row):
                board[row][given_column].remove(number)
        except ValueError:
            pass
    for column in range(BOARD_SIZE):
        try:
            if(column != given_column):
                board[given_row][column].remove(number)
        except ValueError:
            pass

    box_row = given_row // 3
    box_column = given_column // 3

    for row in range(box_row * 3, (box_row + 1) * 3):
        for column in range(box_column * 3, (box_column + 1) * 3):
            try:
                if(row != given_row and column != given_column):
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
            if(len(occurs_at) == 1):
                board[row][occurs_at[0]] = [number]
                update_candidates(board, row, occurs_at[0], number)

    #check for hidden single in a column
    for column in range(BOARD_SIZE):
        for number in range(1, 10):
            occurs_at = []
            for row in range(BOARD_SIZE):
                if number in board[row][column]:       
                    occurs_at.append(row)
            if(len(occurs_at) == 1):
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
                if(len(occurs_at) == 1):
                    board[occurs_at[0][0]][occurs_at[0][1]] = [number]
                    update_candidates(board, occurs_at[0][0], occurs_at[0][1], number)
    
def locked_candidates(board):
    pass