"""Class to manage the state of the game"""
from dataclasses import dataclass
from config import BASE_SPEED

@dataclass
class GameState:
    score:int = 0
    level:int = 0
    lines:int = 0
    is_running : bool =  False
    speed_time:float = BASE_SPEED

    def add_lines(self, count: int):
        self.lines += count
        self.level = self.lines // 10

    def add_score(self, lines_cleared: int, rule: dict):
        points = rule.get(lines_cleared, 0)
        self.score += points * max(1, self.level)
    
    def update_level(self):
        self.level = self.lines // 10