# CLI Tetris written in Python

import random

cols, rows = 10, 20 

grid = [["." for _ in range(cols)]for _ in range(rows)]

TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
}
class CurrentPiece:
    def __init__(self,shape):
        self.shape = shape
        self.position = [round(cols/2),0]
        pass
    
    def get_covered_cells(self):
        covered_cells = []
        for y,part in enumerate(self.shape):
            for x,cell in enumerate(part):
                covered_cells.append([self.position[0] + y,self.position[1]+x])
        return covered_cells
                
    def move_down(self):
        return
    def rotate(self):
        return
    
    
class Board:
    def __init__(self):
        self.board =  [[". " for _ in range(cols)]for _ in range(rows)]
        pass
    
    def draw_board(self,current_piece : CurrentPiece):
      display = self.board.copy()
      for y,part in enumerate(current_piece.shape):
        for x,cell in enumerate(part):
            if cell == 1:
                display[current_piece.position[1]+y][current_piece.position[0]+x] = '[]'
      for row in display:
        print('<!' +' '.join(row) + '!>')
      print()

    


def get_random_piece():
    return random.choice(list(TETROMINOES.values()))
              
def main():
    current_piece = CurrentPiece(get_random_piece())
    print( current_piece.shape)
    print(current_piece.get_covered_cells())
    board = Board()
    board.draw_board(current_piece)

""

if __name__ == "__main__":
    main()