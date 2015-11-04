'''world for a simple harvesting task'''

import random
import copy as cp

class Patch:
    '''a resource patch'''
    def __init__(self, identity, reward, cap_max):
        self.identity = identity
        self.reward = reward
        self.cap_max = cap_max
        self.cap_bound = random.randint(0, self.cap_max)
        self.cap_cur = 0
        # assigned_agent
        self.agents = []

    def assign_agent(self, agent):
        self.cap_cur += 1
        self.agents.append(cp.deepcopy(agent))

    def change_bound(self):
        # reset current capacity
        self.cap_cur = 0
        self.cap_bound = random.randint(0, self.cap_max)

    def has_capacity(self):
        return self.cap_cur < self.cap_bound
    
    def count_reward(self):
        return self.cap_cur * self.reward
    
    def count_violation(self):
        return max(self.cap_cur - self.cap_bound, 0) 

    def return_agents(self, agents):
        for agent in self.agents[:]:
            agents.append(cp.deepcopy(agent))
            self.agents.remove(agent)

class Agent:
    def __init__(self, identity):
        self.identity = identity
