# CLI Tetris written in Python


cols, rows = 10, 20 

grid = [["." for _ in range(cols)]for _ in range(rows)]

TETROMINOS = {
    "I" : [[1,1,1,1]],
    "O" : [[1,1],
           [1,1]],
    "L": [[1,0,0,0],
          [1,1,1,1]],
    "J" : [[0,0,0,1],
           [1,1,1,1]],
    "P": [[0,1,0],
          [1,1,1]]
}



def draw_grid():
    for row in grid:
        print('<!' +' '.join(row) + '!>')
    
              
def main():
    draw_grid()


if __name__ == "__main__":
    main()