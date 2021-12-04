from constants import *

def get_number_in_row(board, number, row, format):
    occurs_at = []
    for col in range(BOARD_SIZE):
        if number in board[row][col]:
            if format == 1:
                occurs_at.append(col)
    return occurs_at


def get_number_in_column(board, number, col, format):
    occurs_at = []
    for row in range(BOARD_SIZE):
        if number in board[row][col]:
            if format == 1:
                occurs_at.append(row)
    return occurs_at


def get_number_in_box(board, number, row_mult, col_mult, format):
    occurs_at = []
    for row in range(row_mult * 3, (row_mult + 1) * 3):
        for col in range(col_mult * 3, (col_mult + 1) * 3):
            if number in board[row][col]:
                if format == 1:
                    occurs_at.append([row, col]) 
                elif format == 2:
                    occurs_at.append((row, col)) 
    return occurs_at


def get_numbers_box(position):
    return [position[0] // 3, position[1] // 3]


def get_n_valued_cells(board, n):
    cells = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if len(board[row][col]) == n:
                cells.append([[row, col], board[row][col]])
    return cells


def get_n_valued_cells_row(board, row, n):
    cells = []
    for col in range(BOARD_SIZE):
        if len(board[row][col]) == n:
            cells.append([col, board[row][col]])
    return cells


def get_n_valued_cells_col(board, col, n):
    cells = []
    for row in range(BOARD_SIZE):
        if len(board[row][col]) == n:
            cells.append([row, board[row][col]])
    return cells


def get_n_valued_cells_box(board, box_row, box_col, n):
    cells = []
    for row in range(3 * box_row, 3 * (box_row + 1)):
        for col in range(3 * box_col, 3 * (box_col + 1)):
            if len(board[row][col]) == n:
                cells.append([[row, col], board[row][col]])
    return cells
    