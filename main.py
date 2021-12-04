from converter import *
from board import *
from techniques import *  
from engine import *

AMOUNT_TO_SOLVE = 100
DIFFICULTY = 2 # 0 - easy, 1 - medium, 2 - hard, 3 - diabolical
MAX_TO_PRINT = 10

def test_single(str):
    board = Board(str, 0)
    engine = Engine(board)
    """ states = engine.states
    for x in range(len(states)):
        if x == 0:
            for line in states[x]:
                print(line)
        else:
            print(states[x][0])
            for line in states[x][1]:
                print(line) """
    board.print()
    

correct = 0
not_complete = 0
empty = 0
correct_ones = []
not_complete_ones = []
empty_ones = []

test_single("..4.....25.8...7.1....3..6.95.47.......3.1.......82.75.6..2....2.9...4.38.....6..")
with open(f'Puzzle bank\{FILE_NAMES[DIFFICULTY]}_converted.txt', 'r') as f:
    sudokus = f.readlines()
    index = 1
    for sudoku in sudokus:
        if AMOUNT_TO_SOLVE == 0: break
        board = Board(strip_sudoku(sudoku), get_number(sudoku))
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
            correct_ones.append([sudoku.split()[0], sudoku.split()[2]])
        index += 1
        if(index > AMOUNT_TO_SOLVE): break


print("correct: {}, not_complete: {}, empty: {}".format(correct, not_complete, empty))
if len(correct_ones) > MAX_TO_PRINT:
    print(correct_ones[:MAX_TO_PRINT])
elif len(correct_ones) > 0:
    print(correct_ones)

if len(not_complete_ones) > MAX_TO_PRINT:
    print(not_complete_ones[:MAX_TO_PRINT])
elif len(not_complete_ones) > 0:
    print(not_complete_ones)

if len(empty_ones) > MAX_TO_PRINT:
    print(empty_ones[:MAX_TO_PRINT])
elif len(empty_ones) > 0:
    print(empty_ones)

