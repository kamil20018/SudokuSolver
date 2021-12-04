from constants import *

def convert_sudoku_files():
    for file_name in FILE_NAMES:
        with open('SudokuSolver\Puzzle bank\\' + file_name + '.txt', 'r') as f1:
            data = f1.readlines()
            with open('SudokuSolver\Puzzle bank\\' + file_name + '_converted.txt', 'w') as f2:
                print(len(data))
                for x in range(len(data)):
                    line = data[x]
                    line = line.split()
                    line[1] = line[1].replace("0", ".")
                    new_line = ""
                    index = 0
                    for char in line[1]:
                        index += 1
                        new_line += char
                        if(index % 9 == 0): new_line += "/"
                    new_line = new_line[:-1]
                    line[1] = new_line
                    line.pop(0)
                    line = " ".join(line)
                    f2.write(str(x + 1) + " " + line + "\n")


def strip_sudoku(sudoku):
    return sudoku.split()[1]


def get_number(sudoku):
    return sudoku.split()[0]