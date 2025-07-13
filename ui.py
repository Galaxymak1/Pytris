"""Manage the rendering/UI of the game"""

from rich.live import Live
from rich.table import Table
from rich.align import Align
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Group,Console
from rich.padding import Padding
from config import BLOCK_MAP
from state import ScreenMode
import os

class UI:
    def __init__(self):
        self.console = Console()
        pass


    def generate_render_grid(self,grid,current_piece):
        render_grid = [row.copy() for row in grid]
        for y, part in enumerate(current_piece.shape):
            for x, cell in enumerate(part):
                if cell == 1:
                    render_grid[current_piece.position[1] + y][current_piece.position[0] + x] = \
                          ("[]", current_piece.color)
        return render_grid
    
    def generate_game_screen(self,game):
        stats = f"[bold green]LEVEL:[/] {game.state.level}    [bold yellow]SCORE:[/] {game.state.score}      [bold blue]LINE CLEARED:[/] {game.state.lines}"

        table = self.generate_table(self.generate_render_grid(game.board.board,game.current_piece))
        next_piece_group = self.generate_next_piece(game.next_piece)

        sidebar = Group(Panel(stats,title="STATS"),Panel(Align.center(next_piece_group),title="NEXT PIECE"))
        layout = Layout()

        layout.split_row(
            Layout(Align.center(table), name="left",size=30),
            Layout(sidebar, name="right", size=20)
        )

        return Group(
                    Align.center(Panel("[bold blue]PYTRIS[/]", expand=False,
                                       border_style="blue")),
                    layout,
                )
        
    def generate_menu_screen(self):
        return Align.center(
            Panel(
                "[bold cyan]Welcome to Pytris![/]\n\n[green]Press 's' to start[/]\n[red]Press 'q' to quit[/]",
                title="Menu",
                border_style="blue",
                padding=(1, 4)
            )
        )

    def generate_game_over_screen(self, score):
        return Align.center(
            Panel(
                f"[bold red]Game Over![/]\n\nFinal Score: [yellow]{score}[/]\n\n[green]Press 'r' to restart\n[red]Press 'q' to quit[/]",
                title="Game Over",
                border_style="red",
                padding=(1, 4)
            )
        )
    
    def generate_next_piece(self,next_piece) -> Table:
        table = Table(
            show_header=False,
            show_lines=False,
            box=None,
            pad_edge=False,
            expand=False,
            padding=(0, 0), 
        )
        shape, color = next_piece
        for row in shape:
            table.add_row(*[BLOCK_MAP.get(color) if cell == 1 else "" for cell in row])
        return table
              


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
            row_cells = []
            for cell in row:
                if cell is None:
                    row_cells.append("⬜")
                else:
                    _, color = cell
                    block = BLOCK_MAP.get(color, "■")  
                    row_cells.append(block)

            table.add_row(*row_cells)
        return Panel(Padding(table,1))
    
    def generate_screen(self, game):
        mode = game.state.screen
        if mode == ScreenMode.MENU:
            return self.generate_menu_screen()
        elif mode == ScreenMode.PLAYING:
            return self.generate_game_screen(game)
        elif mode == ScreenMode.GAME_OVER:
            return self.generate_game_over_screen(game.state.score)

    def render(self, game):
        with Live(self.generate_screen(game), console=self.console, refresh_per_second=30) as live:
            while game.state.is_running:
                live.update(self.generate_screen(game))
                game.clear_full_line()


    def clear_screen(self):
        if os.name == 'nt': 
            os.system('cls')
        else:  
            os.system('clear')