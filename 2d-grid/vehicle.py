from config import *

class Vehicle:
    def __init__(self, start_pos, dest_pos, world):   
        self.pos = cp.deepcopy(start_pos)
        self.dest_pos = dest_pos
        # the world this agent lives in
        self.world = world

    def move(self, action):
        
        # based on the current traffic, the agent will have some probabiltiy to stay
        if random.random() > congest(): return #TBD

        if (action == UP):self.pos[ROW] -=1
        if (action == DOWN):self.pos[ROW] +=1
        if (action == LEFT):self.pos[COL] -=1
        if (action == RIGHT):self.pos[COL] +=1

        # check that the agent cannot move out of boundary
        if (self.pos[ROW] >= self.world.rows):self.pos[ROW] = self.world.rows - 1;
        if (self.pos[ROW] < 0):self.pos[ROW] = 0;
        if (self.pos[COL] >= self.world.columns):self.pos[COL] = self.world.columns - 1;        
        if (self.pos[COL] < 0):self.pos[COL] = 0;

        # check that the agent cannot move offroad


    def draw(self):
        pass

if __name__ == '__main__':
    main()

