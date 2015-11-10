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
        self.agents.append(agent)

    def change_bound(self):
        # reset current capacity
        self.cap_cur = 0
        self.cap_bound = random.randint(0, self.cap_max)

    def has_capacity(self):
        return self.cap_cur < self.cap_bound
    
    def count_reward(self):
        return min(self.cap_cur,self.cap_bound) * self.reward
    
    def count_violation(self):
        return max(self.cap_cur - self.cap_bound, 0) 
    
    def remove_agent(self, agent):
        self.cap_cur -= 1
        self.agents.remove(agent)

    def return_agents(self, another_patch):
        ''' return all agents to home patch '''
        for agent in self.agents[:]:
            another_patch.assign_agent(agent)
            self.agents.remove(agent)
        self.cap_cur = 0

class Agent:
    def __init__(self, identity):
        self.identity = identity
        # temporarily save assigned patch index
        self.assigned_patch = 0
    
    def assign_to(self, index):
        self.assigned_patch = index
