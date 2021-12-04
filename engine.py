from constants import *
import techniques
import copy
class Engine:
    def __init__(self, board):
        self.board = board
        self.solved = self.solve()
        self.board = self.solved[0]
        self.states = self.solved[1]

    def solve(self):
        able_to_solve = True
        board_states = [copy.deepcopy(self.board.board)]
        while(not self.board.is_complete() and able_to_solve):
            for tech in TECHNIQUES:
                technique = getattr(techniques, tech)
                old_board = copy.deepcopy(self.board.board)
                technique(self.board.board)
                if(old_board != self.board.board): 
                    #if tech != 'remove_candidates':
                    board_states.append([tech, copy.deepcopy(self.board.board)])
                    break
                if(tech == TECHNIQUES[-1] and old_board == self.board.board):
                    able_to_solve = False
                    break
        return (self.board, board_states)

    def print(self):
        self.board.print()
