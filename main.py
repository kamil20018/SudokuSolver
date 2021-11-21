from converter import *
from board import *
from techniques import *  
from engine import *

AMOUNT_TO_SOLVE = 1000

def test_single(str):
    board = Board(str)
    Engine(board)
    board.print()

correct = 0
not_complete = 0
empty = 0
not_complete_ones = []
empty_ones = []
with open('Puzzle bank\medium_converted.txt', 'r') as f:
    sudokus = f.readlines()
    index = 1
    for sudoku in sudokus:
        index += 1
        if(index > AMOUNT_TO_SOLVE): break
        board = Board(strip_sudoku(sudoku))
        engine = Engine(board)
        if(not board.is_complete()):
            if(board.is_proper()):
                not_complete += 1
                not_complete_ones.append([sudoku.split()[0], sudoku.split()[2]])
            else:
                empty += 1
                empty_ones.append([sudoku.split()[0], sudoku.split()[2]])
        else:
            correct += 1


print("correct: {}, not_complete: {}, empty: {}".format(correct, not_complete, empty))
print(not_complete_ones)
print(empty_ones)
