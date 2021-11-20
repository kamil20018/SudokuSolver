# SudokuSolver
Terrible sudoku solver with spaghetti code and performance issues - if it's unable to figure out next step it will stop working, it never makes random guesses

Puzzles used to test the software were taken from this repository: https://github.com/grantm/sudoku-exchange-puzzle-bank

Current performance status:
- 100% of easy sudokus solved
- 70% of medium sudokus solved
- 0% of hard sudokus solved
- 0% of diabolical sudokus solved

Average time required to solve 10000 puzzles by difficulty (only counted if 100% of puzzles were solved):
- easy: 35s
- medium: -
- hard: -
- diabolical: -

Todo:
- adding as many advanced solving techniques as possible
- option to display techniques which software needed to solve the puzzle
- gui (may never happen, I hate working with ui)
