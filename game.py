"""Game class that holds main logic"""

import random,time,msvcrt,threading
from threading import Thread

from piece import CurrentPiece
from board import Board
from ui import UI
from player import Player
from config import COLS,ROWS,TETROMINOES,BASE_SPEED,SCORE_RULE,SOUNDS,MUSIC
from state import GameState,ScreenMode



class Game:
    def __init__(self):
        self.state = GameState()
        self.board = Board()
        self.ui = UI()
        self.player = Player()
        self.pieces_pool = list(TETROMINOES.values())
        self.current_piece = CurrentPiece(*self.get_random_piece())
        self.next_piece = self.get_random_piece()
        self.lock = threading.Lock()
        self.input_thread = None
        self.drop_thread = None

        pass
        
    def clear_full_line(self):
        line_cleared = 0
        for x in range(ROWS-1,0,-1):
            if all(cell is not None for cell in self.board.board[x]):
                self.player.play_sound(SOUNDS["line_cleared"],0.6)
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
                    can_rotate =self.current_piece.rotate(self.board.board)
                    if can_rotate and self.current_piece.color != "yellow":
                        self.player.play_sound(SOUNDS["rotation"],0.5)
            

    def auto_drop(self):
        while self.state.is_running:
            with self.lock:
                if self.board.try_move_piece(self.current_piece,"DOWN"):
                    self.get_new_piece()
                    if not self.current_piece.is_position_valid(self.board.board,self.current_piece.position,self.current_piece.shape):
                        self.player.play_sound(SOUNDS["game_over"],0.7)
                        self.state.is_running = False
            self.tick()

    def get_new_piece(self):
        self.current_piece = CurrentPiece(*self.next_piece)
        self.next_piece = self.get_random_piece()

    def tick(self):
        time.sleep(self.state.speed_time) 

    def get_random_piece(self):
        if len(self.pieces_pool) == 0:
            self.pieces_pool = list(TETROMINOES.values())
        index = random.randint(0,len(self.pieces_pool) -1)
        shape,color = self.pieces_pool.pop(index)
        return shape,color


    def wait_for_key(self, valid_keys):
        while True:
            key = self.get_input()
            if key and key in valid_keys:
                return key

    def reset_game(self):
        self.state = GameState()
        self.board = Board()
        self.pieces_pool = list(TETROMINOES.values())
        self.current_piece = CurrentPiece(*self.get_random_piece())
        self.next_piece = self.get_random_piece()

    def main_loop(self):
        self.player.play_menu_music()
        while True:
            self.ui.clear_screen()
            
            if self.state.screen == ScreenMode.MENU:
                self.ui.console.print(self.ui.generate_menu_screen())
                choice = self.wait_for_key({'s', 'q'})
                if choice == 'q':
                    break
                self.reset_game()
                self.player.play_game_music()
                self.state.screen = ScreenMode.PLAYING
                continue

            if self.state.screen == ScreenMode.PLAYING:
                self.state.is_running = True
                self.input_thread = Thread(target=self.handle_input, daemon=True)
                self.drop_thread  = Thread(target=self.auto_drop,   daemon=True)
                self.input_thread.start()
                self.drop_thread.start()

                self.ui.render(self)

                self.input_thread.join()
                self.drop_thread.join()
                self.player.stop_music()
                self.state.screen = ScreenMode.GAME_OVER
                continue

            if self.state.screen == ScreenMode.GAME_OVER:
                self.ui.console.print(self.ui.generate_game_over_screen(self.state))
                choice = self.wait_for_key({'r', 'q'})
                if choice == 'r':
                    self.reset_game()
                    self.player.play_game_music()
                    self.state.screen = ScreenMode.PLAYING
                    continue
                else:
                    break

        self.ui.clear_screen()
        self.ui.console.print("Goodbye!")



