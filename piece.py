"""Current Piece class"""

from config import COLS,ROWS

class CurrentPiece:
    def __init__(self,shape,color):
        self.shape = shape
        self.position = [COLS // 2 - 2,0]
        self.color = color
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
            if (
                cell[1] >= ROWS
                or cell[0] < 0
                or cell[0] >= COLS
                or grid[cell[1]][cell[0]] is not None
            ):
                return False
        return True
    
    
    def rotate(self,grid):
        future_shape = [row.copy() for row in self.shape]
        rotated_future_shape = [list(row) for row in zip(*future_shape[::-1])]
        if not self.is_position_valid(grid,self.position,rotated_future_shape):
            return
        self.shape = rotated_future_shape
        return