from config import *
import world

class Car:
    def __init__(self, identity, start, dest, world, car_type):   
        self.identity = identity
        self.pos = cp.deepcopy(start)
        self.dest = cp.deepcopy(dest)
        self.car_type = car_type
        self.cap = CAP_CAR[self.car_type]
        # the world this agent lives in
        self.world = world
        # update road block
        self.world.world_map[self.pos[ROW]][self.pos[COL]].add_car()

    def move(self, action):
        if (self.world.success_move(self.pos, action)):
            self.world.world_map[self.pos[ROW]][self.pos[COL]].rm_car()
            if (action == UP):
                self.pos[ROW] -=1
            if (action == DOWN): 
                self.pos[ROW] +=1
            if (action == LEFT):
                self.pos[COL] -=1
            if (action == RIGHT):
                self.pos[COL] +=1
            # if action is STAY nothing happens
            self.world.world_map[self.pos[ROW]][self.pos[COL]].add_car()
    
    def greedy_act(self):
        '''choose the action and move; shortest path with random tie-break'''
        '''TBD, car can get stuck now'''
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

    def a_star_act(self):
        '''an a_star (time-based) agent'''
        pass

    def print_status(self):
        print("{:<6}".format(self.identity)),
        print("({:>2}, {:<2})".format(self.pos[ROW], self.pos[COL])), 
        print("({:>2}, {:<2})".format(self.dest[ROW], self.dest[COL])) 

    def draw(self):
        pass

