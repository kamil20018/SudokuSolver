from constants import *
import techniques_app
import techniques_test
import copy
class Engine:
    def __init__(self, board, test):
        self.board = board
        if not test:
            self.solved = self.solve_app()
            self.board = self.solved[0]
            self.states = self.solved[1]
        elif test:
            self.solved = self.solve_test()
            self.board = self.solved

    def solve_app(self):
        able_to_solve = True
        board_states = [copy.deepcopy(self.board.board)]
        while(not self.board.is_complete() and able_to_solve):
            for tech in TECHNIQUES:
                technique = getattr(techniques_app, tech)
                old_board = copy.deepcopy(self.board.board)
                coloring = technique(self.board.board)
                if(old_board != self.board.board): 
                    board_states.append([tech, copy.deepcopy(self.board.board), coloring])
                    break
                if(tech == TECHNIQUES[-1] and old_board == self.board.board):
                    able_to_solve = False
                    break
        return (self.board, board_states)


    def solve_test(self):
        able_to_solve = True
        while(not self.board.is_complete() and able_to_solve):
            for tech in TECHNIQUES:
                technique = getattr(techniques_test, tech)
                old_board = copy.deepcopy(self.board.board)
                technique(self.board.board)
                if(old_board != self.board.board): 
                    break
                if(tech == TECHNIQUES[-1] and old_board == self.board.board):
                    able_to_solve = False
                    break
        return self.board

    def print(self):
        self.board.print()
