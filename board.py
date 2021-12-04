from constants import *

class Board:
    def __init__(self, board_string, number):
        self.number = number
        self.board_string = board_string.split("/")
        self.board = self.string_to_num(self.board_string)
        self.board = self.fill_candidates(self.board)

    def string_to_num(self, board_string):
        if len(board_string) == 1: #sudoku in the format without "/" can still be parsed
            board_string = [board_string[0][i:i+9] for i in range(0, len(board_string[0]), 9)]
        board = []
        for row in board_string:
            line = []
            for char in row:
                if char == ".":
                    line.append([])
                else:
                    line.append([int(char)])
            board.append(line)
        return board
        

    def fill_candidates(self, board):
        candidates = [x for x in range(1, 10)]
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if(len(board[row][column]) != 1):
                    board[row][column] = candidates.copy()
        return board

    def is_complete(self):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if(len(self.board[row][column]) != 1): return False
        return True
    
    def is_proper(self):
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                if(len(self.board[row][column]) < 1): return False
        return True

    def print(self):
        for line in self.board:
            print([x[0] if len(x) == 1 else x for x in line])
            