# SudokuSolver
Warning: the size of entire repo is big because of puzzle bank: there are 1000000+ sudokus stored there

This solver uses pure, human logic to solve sudoku puzzles. It visualizes and names techniquest that it used to solve the puzzle

Waring: the performance of current build is much worse - I've modified the way some of the techniques work, so that the logic behind them will be much more visible in the app.
If you want the solver to solve puzzles from the puzzle bank, run main.py.
If you want the solver to run an app with gui and custom puzzle input, run app.py

Puzzles used to test the software were taken from this repository: https://github.com/grantm/sudoku-exchange-puzzle-bank

Implemented techniques:
- hidden single
- locked candidates (pointing and claiming)
- naked pairs
- naked triples
- naked quadruples
- hidden pairs
- hidden triples
- hidden quadruples
- x-wing
- skyscraper
- 2-string kite

Current performance status:
- 100% of easy sudokus solved
- 100% of medium sudokus solved
- 65% of hard sudokus solved
- 0% of diabolical sudokus solved

Average time required to solve 10000 puzzles by difficulty (only counted if 100% of puzzles were solved):
- easy: 35s
- medium: 58s
- hard: -
- diabolical: -

Todo:
- adding as many advanced solving techniques as possible
- ~~option to display techniques which software needed to solve the puzzle~~ - done
- technique explaination in sidebar
