"""Game class that holds main logic"""

import random,time,msvcrt,threading
from threading import Thread


from piece import CurrentPiece
from board import Board
from ui import UI
from config import COLS,ROWS,TETROMINOES,BASE_SPEED,SCORE_RULE
# from main import play_music
from state import GameState



class Game:
    def __init__(self):
        self.state = GameState()
        self.board = Board()
        self.ui = UI()
        self.current_piece = CurrentPiece(*get_random_piece())
        self.next_piece = get_random_piece()
        self.lock = threading.Lock()
        pass
        
    def clear_full_line(self):
        line_cleared = 0
        for x in range(ROWS-1,0,-1):
            if all(cell is not None for cell in self.board.board[x]):
                self.board.board.pop(x)
                self.board.board.insert(0, [None for _ in range(COLS)])
                line_cleared += 1
        self.update_score(line_cleared)
    
    def update_score(self,line_cleared):
        if line_cleared == 0: return
        self.state.add_lines(line_cleared)
        self.state.update_level()
        self.state.add_score(line_cleared,SCORE_RULE)
                
    def update_speed(self):
        self.state.speed_time = max(0.05, BASE_SPEED - 0.05 * self.level)

    def get_input(self):
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
                
    def handle_input(self):
        while self.state.is_running:
            input = self.get_input()
            if input == "q":
                self.state.is_running = False
                break
            elif input == "LEFT" or input == "RIGHT" :
                with self.lock:
                    self.board.try_move_piece(self.current_piece,input)
            elif input == "DOWN":
                if not self.board.try_move_piece(self.current_piece,input):
                    self.state.score += 1 * self.state.level + 1
            elif input == "UP":
                with self.lock:
                    self.current_piece.rotate(self.board.board)
            

    def auto_drop(self):
        while self.state.is_running:
            with self.lock:
                self.clear_full_line()
                if self.board.try_move_piece(self.current_piece,"DOWN"):
                    self.get_new_piece()
                    if not self.current_piece.is_position_valid(self.board.board,self.current_piece.position,self.current_piece.shape):
                        self.state.is_running = False
            self.tick()

    def get_new_piece(self):
        self.current_piece = CurrentPiece(*self.next_piece)
        self.next_piece = get_random_piece()

    def tick(self):
        time.sleep(self.state.speed_time) 

        

    def main_loop(self):
        self.ui.clear_screen()
        Thread(target=self.handle_input).start()
        Thread(target=self.auto_drop).start()
        # Thread(target=play_music, args=("tetris_theme.mp3",), daemon=True).start()
        
        self.ui.render(self)

def get_random_piece():
    shape,color = random.choice(list(TETROMINOES.values()))
    return shape,color