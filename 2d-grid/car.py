from config import *
import world

class Car:
    def __init__(self, identity, start, dest, world):   
        self.identity = identity
        self.pos = cp.deepcopy(start)
        self.dest = cp.deepcopy(dest)
        # the world this agent lives in
        self.world = world
        # update road block
        self.world.world_map[self.pos[ROW]][self.pos[COL]].add_car()

    def move(self, action):
        if (self.world.legal(self.pos, action)):
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
    
    def choose_act_move(self):
        '''choose the action and move; it should be an RL-based agent but in this simple world it is just follow shortest distance'''
        dists = []
        for action in ACTIONS:
            dists.append(self.world.dist_act(self.pos, action, self.dest))
        best = [0]
        for i in range(len(ACTIONS)):
            if dists[i] < dists[best[0]]: best[:] = [i]
            elif dists[i] == dists[best[0]]: best.append(i)
        if len(best) == 1: act = best[0]
        elif len(best) > 1: act = random.choice(best)
        self.move(act)

    def print_status(self):
        print("{:<6}".format(self.identity)),
        print("({:>2}, {:<2})".format(self.pos[ROW], self.pos[COL])), 
        print("({:>2}, {:<2})".format(self.dest[ROW], self.dest[COL])) 

    def draw(self):
        pass
