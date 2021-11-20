from constants import *
import techniques
import copy
class Engine:
    def __init__(self, board):
        self.board = board
        self.board = self.solve()

    def solve(self):
        able_to_solve = True
        while(not self.board.is_complete() and able_to_solve):
            for tech in TECHNIQUES:
                technique = getattr(techniques, tech)
                old_board = copy.deepcopy(self.board.board)
                technique(self.board.board)
                if(old_board != self.board.board): break #no need to try tougher techniques if easier ones succeded in removing some of the candidates
                if(tech == TECHNIQUES[-1] and old_board == self.board.board):
                    able_to_solve = False
                    break
            
        return self.board
        

    def print(self):
        self.board.print()
