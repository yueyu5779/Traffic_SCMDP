from config import *

class Block:
    def __init__(self, pos, block_type, capacity):
        self.pos = cp.deepcopy(pos)
        self.block_type = block_type
        # capacity upper bound
        self.cap_bound = capacity 
        # store the vehicles in this block
        self.cap_cur = 0
    
    def rm_car(self):
        self.cap_cur -= 1

    def add_car(self):
        self.cap_cur += 1

    def congest(self):
        '''return true if a car can successfuly move into the block, based on current traffic capacity'''
        return random.random() < 1 - (self.cap_cur + DEF_TRAFFIC) / self.cap_bound

class World:
    def __init__(self):
        self.rows = (len(CAP_HZ_ROAD) - 1) * (NUM_BLK_BTW + 1) + 1
        self.columns = (len(CAP_VT_ROAD) - 1) * (NUM_BLK_BTW + 1) + 1
        # represent map as a 2D array
        self.world_map = [[0 for x in range(self.columns)] for x in range(self.rows)]
        self.construct_map()

    def construct_map(self):
        ''' construct the world map by defining each block'''
        # fill in the horizontal roads
        for i in range(len(CAP_HZ_ROAD)):
            cur_row = i * (NUM_BLK_BTW + 1)
            for j in range(self.columns):
                self.world_map[cur_row][j] = Block([cur_row, j], ROAD, CAP_HZ_ROAD[i])    
        # fill in the vertical roads
        for i in range(len(CAP_HZ_ROAD)):
            cur_col = i * (NUM_BLK_BTW + 1)
            for j in range(self.rows):
                self.world_map[j][cur_col] = Block([j, cur_col], ROAD, CAP_VT_ROAD[i])    

        # fill in the intersections
        for i in range(len(CAP_HZ_ROAD)):
            for j in range(len(CAP_VT_ROAD)):
                # the position of the intersection that ith and jth roads cross
                ij_pos = [i * (NUM_BLK_BTW + 1), j * (NUM_BLK_BTW + 1)]
                # calculate capacity
                # four conrner intersects
                if ((i == 0 and j == 0) or \
                (i == 0 and j == len(CAP_VT_ROAD) - 1) \
                or (i == len(CAP_HZ_ROAD) - 1 and j == 0) \
                or (i == len(CAP_HZ_ROAD) -1 and j == len(CAP_VT_ROAD) - 1)):
                    cap = CAP_HZ_ROAD[i] + CAP_VT_ROAD[j]
                # Top and bottom intersects but not corners
                elif (i == 0) or (i == len(CAP_HZ_ROAD) - 1): 
                    cap = CAP_HZ_ROAD[i] * 2 + CAP_VT_ROAD[j]
                # Leftmost and rightmost intersects but not corners
                elif (j == 0) or (j == len(CAP_VT_ROAD) - 1): 
                    cap = CAP_HZ_ROAD[i] + CAP_VT_ROAD[j] * 2
                # other intersects
                else: cap = (CAP_HZ_ROAD[i] + CAP_VT_ROAD[j]) / 2
                self.world_map[ij_pos[ROW]][ij_pos[COL]] = Block(ij_pos, INTERSECT, cap)    

        # fill in the rest of the map by OFFROAD
        for i in range(self.rows):
            for j in range(self.columns):
                if self.world_map[i][j] == 0:
                    self.world_map[i][j] = Block([i,j], OFFROAD, 0) 
 
    def legal(self, agent_pos, action):
        '''determine whether an action of the agent is legal'''
        if action == UP: pos = [agent_pos[ROW] - 1, agent_pos[COL]]
        elif action == DOWN: pos = [agent_pos[ROW] + 1, agent_pos[COL]]
        elif action == LEFT: pos = [agent_pos[ROW], agent_pos[COL] - 1]
        elif action == RIGHT: pos = [agent_pos[ROW], agent_pos[COL] + 1]
        '''check if a move to a new pos is legal'''
        # check that the agent cannot move out of boundary
        if (pos[ROW] >= self.rows): return False
        if (pos[ROW] < 0): return False
        if (pos[COL] >= self.columns): return False
        if (pos[COL] < 0): return False
        # check that the agent cannot move offroad
        if self.world_map[pos[ROW]][pos[COL]].block_type == OFFROAD: return False
        # check the traffic
        return self.world_map[pos[ROW]][pos[COL]].congest()

    def dist(self, start_pos, dest_pos):
        '''get the distance between two positions'''
        return abs(start_pos[ROW] - dest_pos[ROW]) + abs(start_pos[COL] - dest_pos[COL])

    def dist_act(self, agent_pos, action, dest_pos):
        '''return the resulted distance after taking an action in the current map'''
        if self.legal(agent_pos, action):
            if action == UP: pos = [agent_pos[ROW] - 1, agent_pos[COL]]
            elif action == DOWN: pos = [agent_pos[ROW] + 1, agent_pos[COL]]
            elif action == LEFT: pos = [agent_pos[ROW], agent_pos[COL] - 1]
            elif action == RIGHT: pos = [agent_pos[ROW], agent_pos[COL] + 1]
            return self.dist(pos, dest_pos)
        else: return self.dist(agent_pos, dest_pos)

    def print_cap_map(self):
        '''print capacity map in a table form'''
        for i in range(self.rows):
            for j in range(self.columns):
                print('{:>4}'.format(self.world_map[i][j].cap_bound)),
            print('\n')

    def draw(self, isNew = False):
        CELL_SIZE = 40
        if isNew:
            width_ = (self.columns + 2) * CELL_SIZE
            height_ = (self.rows + 2) * CELL_SIZE
            # Draw map cells:
            self.window = cg.GraphWin(title = "City Map", width = width_, height = height_)
            # Draw position labels
            # Row labels
            for i in range(self.rows):
                label = cg.Text(cg.Point((self.columns + 0.5) * CELL_SIZE, (i + 0.5) * CELL_SIZE),str(i))
                label.draw(self.window)
            # Column labels
            for i in range(self.columns):
                label = cg.Text(cg.Point((i + 0.5) * CELL_SIZE, (self.rows + 0.5) * CELL_SIZE),str(i))
                label.draw(self.window)

        # Draw capacity bound at upper left corner and current capacity at lower right corner
        for i in range(self.rows):
            for j in range(self.columns):
                if self.world_map[i][j].block_type != OFFROAD:
                    block = cg.Rectangle(cg.Point(j * CELL_SIZE, i * CELL_SIZE), cg.Point((j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE))
                    # normal traffic situation
                    if self.world_map[i][j].cap_bound > self.world_map[i][j].cap_cur: 
                        block.setFill("lightblue")
                    else: # traffic jam
                        block.setFill("pink")
                    block.draw(self.window)
                    cap_bound = cg.Text(cg.Point((j+0.25) * CELL_SIZE, (i+0.25) * CELL_SIZE),str(self.world_map[i][j].cap_bound))
                    cap_bound.setSize(9)
                    cap_bound.setFill("red")
                    cap_bound.draw(self.window)
                    cap_cur = cg.Text(cg.Point((j+0.75) * CELL_SIZE, (i+0.75) * CELL_SIZE),str(self.world_map[i][j].cap_cur))
                    cap_cur.setSize(10)
                    cap_cur.setFill("black")
                    cap_cur.draw(self.window)

if __name__ == '__main__':
    main()
    # test_world = World()
    # test_world.print_cap_map()
    # test_world.draw()
    # raw_input("Print Enter to Exit")
