from config import *
import World

class Car:
    def __init__(self, start_pos, dest_pos, world):   
        self.pos = cp.deepcopy(start_pos)
        self.dest_pos = cp.deepcopy(dest_pos)
        # the world this agent lives in
        self.world = world

    def legal(self, action):
        if action == UP: pos = [self.pos[ROW] - 1, self.pos[COL]]
        elif action == DOWN: pos = [self.pos[ROW] + 1, self.pos[COL]]
        elif action == LEFT: pos = [self.pos[ROW], self.pos[COL] - 1]
        elif action == RIGHT: pos = [self.pos[ROW], self.pos[COL] + 1]
        '''check if a move to a new pos is legal'''
        # check that the agent cannot move out of boundary
        if (pos[ROW] >= self.world.rows): return False
        if (pos[ROW] < 0): return False
        if (pos[COL] >= self.world.columns): return False
        if (pos[COL] < 0): return False
        # check that the agent cannot move offroad
        if self.world.world_map[pos[ROW]][pos[COL]].grid_type == OFFROAD: return False
        # check the traffic
        return self.world.world_map[pos[ROW]][pos[COL]].congest()

    def move(self, action):
        if (self.legal(action)):
            self.world.world_map[self.pos[ROW]][self.pos[COL]].rm_car()
            if (action == UP):
                self.pos[ROW] -=1
            if (action == DOWN): 
                self.pos[ROW] +=1
            if (action == LEFT):
                self.pos[COL] -=1
            if (action == RIGHT):
                self.pos[COL] +=1
            self.world.world_map[self.pos[ROW]][self.pos[COL]].add_car()

    def draw(self):
        pass

