'''two dictionaries that quickly matches between state numerate and state vector'''

import numpy as np
import car
import world
from config import *

def to_key(state):
    '''change a state vec to string'''
    if len(state) < 5:
        print("invalid state")
    else:
        key = ""
        for ele in state: 
            key = key + str(ele) + ','
        return key

class StateDict:
    def __init__(self, world):
        self.world = world
        self.state_num = {} # str(list), num type
        self.num_state = {} # str(num), list type
        self.construct_dict()
        self.num_state = len(self.state_num)

    def construct_dict(self):
        state_count = 0
        for i in range(self.world.rows):
            for j in range(self.world.columns):
                if self.world.world_map[i][j].block_type != OFFROAD:
                    for dest in DESTINATION:
                        for car_type in CAR_TYPE:
                            state = [i, j,dest[ROW], dest[COL], car_type]
                            self.state_num[to_key(state)] = state_count
                            self.num_state[str(state_count)] = cp.deepcopy(state)
                            state_count += 1    
    def get_num(self, state):
        '''given a state vector, find its corresponding num, car can use this to get its state num and query policy'''
        return self.state_num[to_key(cp.deepcopy(state))] 

    def get_state(self, num):
        '''give a state number, find its corresponding state vector, when costructing matrices for scmdp this is needed'''
        return cp.deepcopy(self.num_state[str(num)])

    def print_states(self):
        print("dictionary is: ")
        for i in range(len(self.num_state)):
            state = self.get_state(i)
            num = self.get_num(state)
            print(num, state)

if __name__ == "__main__":
    test_world = world.World()
    states = StateDict(test_world)
    states.print_states()

