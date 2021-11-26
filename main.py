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

#test_single("1...7.....3.6....8..21..7...2.....394...8...258.....1...4..79..7....2.8.....6...5")
with open('Puzzle bank\hard_converted.txt', 'r') as f:
    sudokus = f.readlines()
    index = 1
    for sudoku in sudokus:
        if AMOUNT_TO_SOLVE == 0: break
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
        index += 1
        if(index > AMOUNT_TO_SOLVE): break


print("correct: {}, not_complete: {}, empty: {}".format(correct, not_complete, empty))
if len(not_complete_ones) > 12:
    print(not_complete_ones[:11])
elif len(not_complete_ones) > 0:
    print(not_complete_ones)
if len(empty_ones) > 12:
    print(empty_ones[:11])
elif len(not_complete_ones) > 0:
    print(empty_ones)

