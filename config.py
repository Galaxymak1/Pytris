"""config class to hold constants"""


COLS, ROWS = 10, 20
BASE_SPEED = 0.3
SCORE_RULE= {1 : 40,
                     2 : 100,
                     3 : 300,
                     4 : 1200}
TETROMINOES = {
    'I': [[[1, 1, 1, 1]],"cyan"],
    'O': [[[1, 1],
          [1, 1]],"yellow"],
    'T': [[[0, 1, 0],
          [1, 1, 1]],"magenta"],
    'S': [[[0, 1, 1],
          [1, 1, 0]],"green"],
    'Z': [[[1, 1, 0],
          [0, 1, 1]],"red"],
    'J': [[[1, 0, 0],
          [1, 1, 1]],"brown"],
    'L': [[[0, 0, 1],
          [1, 1, 1]],"orange"],
}

BLOCK_MAP = {
    "cyan": "🟦",
    "yellow": "🟨",
    "magenta": "🟪",
    "green": "🟩",
    "red": "🟥",
    "brown": "🟫",
    "orange": "🟧",
}