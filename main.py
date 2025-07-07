# CLI Tetris written in Python

import random,time,os,msvcrt,threading
from threading import Thread

from rich import print
from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Group,Console


cols, rows = 10, 20

base_speed = 0.3

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
    
    def get_covered_cells(self,position,shape):
        covered_cells = []
        for y,part in enumerate(shape):
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
        if not self.is_position_valid(grid,future_position,self.shape):
            if direction in "RIGHT LEFT":
                return False
            else:
                return True
        self.position = future_position
        return False
    
    def is_position_valid(self,grid,position,shape):
        covered_cells = self.get_covered_cells(position,shape)
        for cell in covered_cells:
            if cell[1] >= rows or cell[0] < 0 or cell[0] >= cols or grid[cell[1]][cell[0]] == '[]':
                return False
        return True
    
    
    def rotate(self,grid,direction):
        future_shape = [row.copy() for row in self.shape]
        future_shape = [list(row) for row in zip(*future_shape[::-1])]
        if not self.is_position_valid(grid,self.position,future_shape):
            return
        self.shape = future_shape
        return


    
    
class Board:
    def __init__(self):
        self.board =  [[". " for _ in range(cols)]for _ in range(rows)]
        pass
    


    def try_move_piece(self,current_piece :CurrentPiece, direction : str):
        if current_piece.move(self.board,direction):
            self.land_piece(current_piece)
            return True
        return False
    
    def land_piece(self,current_piece : CurrentPiece):
        cells = current_piece.get_covered_cells(current_piece.position,current_piece.shape)
        for cell in cells:
            self.board[cell[1]][cell[0]] = "[]"


def get_random_piece():
    return random.choice(list(TETROMINOES.values()))


class Game:
    def __init__(self):
        self.score = 0
        self.level = 0
        self.line_cleared = 0
        self.rule = {1 : 40,
                     2 : 100,
                     3 : 300,
                     4 : 1200}
        self.is_game_running = False
        self.board = Board()
        self.sleep_time = base_speed
        self.current_piece = CurrentPiece(get_random_piece())
        self.next_piece = get_random_piece()
        self.console = Console()
        self.lock = threading.Lock()
        pass
        
    def clear_full_line(self):
        line_cleared = 0
        for x in range(rows-1,0,-1):
            if self.board.board[x].count("[]") == cols:
                self.board.board.pop(x)
                self.board.board.insert(0, [". " for _ in range(cols)])
                line_cleared += 1
        self.update_score(line_cleared)
    
    def update_score(self,line_cleared):
        if line_cleared == 0:
            return
        self.line_cleared += line_cleared
        if line_cleared > 10:
            line_cleared - 10
            self.level += 1
        self.score += self.rule[line_cleared] * self.level if self.level > 0 else self.rule[line_cleared]
        
    def update_speed(self):
        self.sleep_time = max(0.05, base_speed - 0.05 * self.level)

    def generate_screen(self):
        display = [row.copy() for row in self.board.board]
        for y, part in enumerate(self.current_piece.shape):
            for x, cell in enumerate(part):
                if cell == 1:
                    display[self.current_piece.position[1] + y][self.current_piece.position[0] + x] = "[]"

        stats = f"[bold green]LEVEL:[/] {self.level}    [bold yellow]SCORE:[/] {self.score}"

        table = self.generate_table(display)
        next_piece_group = self.generate_next_piece()

        layout = Layout()


        layout.split_row(
            Layout(table, name="left",ratio=3),
            Layout(Group(Panel(stats,title="STATS"),Panel(Align.center(next_piece_group),title="NEXT PIECE")), name="right", ratio=1)
        )

        return Group(
                    Align.center(Panel("[bold blue]PETRIS[/]", expand=False, border_style="blue")),
                    layout,
                )
        

    def generate_next_piece(self) -> Table:
        table = Table(
            show_header=False,
            show_lines=False,
            box=None,
            pad_edge=False,
            expand=False,
            padding=(0, 0), 
        )
        for row in self.next_piece:
            table.add_row(*["🟦" if cell == 1 else "" for cell in row])
              


    def generate_table(self,display) -> Table:
        table = Table(
            show_header=False,
            show_lines=False,
            box=None,
            pad_edge=False,
            expand=False,
            padding=(0, 0), 
        )
        for row in display:
            table.add_row(*["🟦" if cell == "[]" else "⬜" for cell in row ])
        return table


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
        while self.is_game_running:
            input = self.get_input()
            if input == "LEFT" or input == "RIGHT" or input == "DOWN":
                with self.lock:
                    self.board.try_move_piece(self.current_piece,input)
            elif input == "UP":
                with self.lock:
                    self.current_piece.rotate(self.board.board,input)

    def auto_drop(self):
        while self.is_game_running:
            with self.lock:
                if self.board.try_move_piece(self.current_piece,"DOWN"):
                    self.get_new_piece()
                    if not self.current_piece.is_position_valid(self.board.board,self.current_piece.position,self.current_piece.shape):
                        self.is_game_running = False
            self.tick()

    def get_new_piece(self):
        self.current_piece = CurrentPiece(self.next_piece)
        self.next_piece = get_random_piece()

    def tick(self):
        time.sleep(self.sleep_time) 

    def render(self):
        with Live(self.generate_screen(), console=self.console, refresh_per_second=20) as live:
            while self.is_game_running:
                with self.lock:
                    self.clear_full_line()
                live.update(self.generate_screen())  
                


    def main_loop(self):
        clear_screen()
        Thread(target=self.handle_input).start()
        Thread(target=self.auto_drop).start()
        self.render()


                        


def game():
    game = Game()
    game.is_game_running =  True
    game.main_loop()
    print("Game Over")
              
def main():
    game()

        

if __name__ == "__main__":
    main()