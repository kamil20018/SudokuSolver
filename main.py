from converter import *
from board import *
from techniques import *  
from engine import *

AMOUNT_TO_SOLVE = 10000

def test_single(str):
    board = Board(str)
    engine = Engine(board)
    board.print()


correct = 0
wrong = 0
wrong_ones = []
with open('SudokuSolver\Puzzle bank\easy_converted.txt', 'r') as f:
    sudokus = f.readlines()
    index = 1
    for sudoku in sudokus:
        board = Board(strip_sudoku(sudoku))
        engine = Engine(board)
        if(not board.is_complete()):
            wrong += 1
            wrong_ones.append([sudoku.split()[0], sudoku.split()[2]])
            #print(sudoku.split()[0]) #sudoku number from the file
            #board.print()
        else:
            correct += 1
        index += 1
        if(index > AMOUNT_TO_SOLVE): break

print("correct: {}, wrong: {}".format(correct, wrong))
print(wrong_ones)