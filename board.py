"""Board class"""

from config import COLS,ROWS
from piece import CurrentPiece


class Board:
    def __init__(self):
        self.board =  [[None for _ in range(COLS)]for _ in range(ROWS)]
        pass
    


    def try_move_piece(self,current_piece :CurrentPiece, direction : str):
        if current_piece.move(self.board,direction):
            self.land_piece(current_piece)
            return True
        return False
    
    def land_piece(self,current_piece : CurrentPiece):
        cells = current_piece.get_covered_cells(current_piece.position,current_piece.shape)
        for cell in cells:
            self.board[cell[1]][cell[0]] = ("[]",current_piece.color)


