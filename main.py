# CLI Tetris written in Python

import random,time,os,msvcrt,asyncio

cols, rows = 10, 20


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

def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')
        
class CurrentPiece:
    def __init__(self,shape):
        self.shape = shape
        self.position = [round(cols/2),0]
        pass
    
    def get_covered_cells(self,position):
        covered_cells = []
        for y,part in enumerate(self.shape):
            for x,cell in enumerate(part):
                if cell == 1:
                    covered_cells.append([position[0] + x, position[1] + y])
        return covered_cells
                
    def move(self,grid,direction):
        future_position = self.position.copy()
        if direction == "DOWN":
            future_position[1] += 1
        if direction == "LEFT":
            future_position[0] -= 1
        if direction == "RIGHT":
            future_position[0] += 1
        if not self.is_position_valid(grid,future_position):
            if direction in "RIGHT LEFT":
                return False
            else:
                return True
        self.position = future_position
        return False
    
    def is_position_valid(self,grid,position):
        covered_cells = self.get_covered_cells(position)
        for cell in covered_cells:
            if cell[1] >= rows or cell[0] < 0 or cell[0] >= cols or grid[cell[1]][cell[0]] == '[]':
                return False
        return True
    
    def rotate(self):
        return
    
    
class Board:
    def __init__(self):
        self.board =  [[". " for _ in range(cols)]for _ in range(rows)]
        pass
    
    def draw_board(self,current_piece : CurrentPiece):
        display = [row.copy() for row in self.board]
        for y,part in enumerate(current_piece.shape):
            for x,cell in enumerate(part):
                if cell == 1:
                    display[current_piece.position[1]+y][current_piece.position[0]+x] = '[]'
        for row in display:
            print('<!' +' '.join(row) + '!>')
        print()

    def try_move_piece(self,current_piece :CurrentPiece, direction : str):
        if current_piece.move(self.board,direction):
            self.land_piece(current_piece)
            return True
        return False


    

    def land_piece(self,current_piece : CurrentPiece):
        cells = current_piece.get_covered_cells(current_piece.position)
        for cell in cells:
            self.board[cell[1]][cell[0]] = "[]"

def clear_full_line(board):
    for y,row in enumerate(board):
        if row.count("[]") == cols:
            board[y] = [". " for _ in range(cols)]


        
        


def handle_input():
        if msvcrt.kbhit():
                key = msvcrt.getch()
                try:
                    return key.decode()
                except UnicodeDecodeError:  
                    if key == b"\xe0":
                        key = msvcrt.getch()
                        if key == b"H":
                            return "UP"
                        if key == b"P":
                            return "DOWN"
                        if key == b"K":
                            return "LEFT"
                        if key == b"M":
                            return "RIGHT"
                    return
                        

def get_random_piece():
    return random.choice(list(TETROMINOES.values()))

def game():
    current_piece = CurrentPiece(get_random_piece())
    print( current_piece.shape)
    board = Board()
    while True:
        input = handle_input()
        if input == "LEFT" or input == "RIGHT":
            board.try_move_piece(current_piece,input)
        if board.try_move_piece(current_piece,"DOWN"):
            current_piece = CurrentPiece(get_random_piece())
            if not current_piece.is_position_valid(board.board,current_piece.position):
                break
        board.draw_board(current_piece)
        time.sleep(0.05)    
        clear_screen()
       
    print("Game Over")
              
def main():
    game()

            


if __name__ == "__main__":
    main()