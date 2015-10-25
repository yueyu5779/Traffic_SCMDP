from config import *

# Enums for the map
OFFROAD = 0
INTERSECT = 1
ROAD = 2
# number of road blocks between 2 intersections
NUM_BLOCK_BTW = 2 

class Block:
    def __init__(self, pos, grid_type, capacity):
        self.pos = cp.deepcopy(pos)
        self.grid_type = grid_type
        self.cap = capacity
        
class World:
    def __init__(self, num_row_intersect, num_col_intersect):
        self.rows = (num_row_intersect - 1) * NUM_BLOCK_BTW + 1
        self.columns = (num_col_intersect - 1) * NUM_BLOCK_BTW + 1

        # represent map as a 2D array
        self.world_map = [[0 for x in range(columns)] for x in range(rows)]
    
        # fill in the map by Block objects


    def draw(self):
        pass
if __name__ == '__main__':
    main()

