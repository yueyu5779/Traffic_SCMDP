'''experiment file'''

import world
import random
import sys
import roulette
import scmdp
import numpy as np

NUM_STATE = 10
HOME = 0
REWARD = [0,10,9,8,7,6,5,4,3,2,1]
# capacity upper bound's upper limit
CAP_MAX_VALUE = 100
CAP_MAX = [CAP_MAX_VALUE for i in range(NUM_STATE - 1)] 
CAP_MAX.insert(0, 9999999) # home, its capacity is the number of agents

NUM_EPISODE = 3
# allocation algorithms
CENTRALIZED = 0
RANDOM = 1
PROB = 2
SCMDP = 3

class Experiment:
    def __init__(self, num_agent, alg):
        self.patches = []
        for i in range(NUM_STATE):
            if i == 0: # home
                new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX[i])
                new_patch.cap_bound = num_agent
            else:
                new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX[i])
            self.patches.append(new_patch)
        self.num_agent = num_agent
        for i in range(self.num_agent):
            new_agent = world.Agent(identity = i)
        # put all agents in patch0 (home)
            self.patches[0].assign_agent(new_agent)
        self.total_reward = 0
        self.violation_count = 0
        self.alg = alg

    def print_patch_status(self):
            '''print status for all patches'''
            print("======================================")
            print("{:<12} {:<12} {:<12} {:<12} {:<12}".format("Reward", "Upperbound", "#agents", "Gained Reward", "Violations"))
            for patch in self.patches:
                print("{:<12} {:<12} {:<12} {:<12} {:<12}".format(patch.reward, patch.cap_bound, patch.cap_cur, patch.cap_cur * patch.reward, patch.count_violation()))
            print("--------------------------------------")
            print("{:<12} {:<12}".format("Volations", "Total Reward"))
            print("{:<12} {:<12}".format(self.violation_count,self.total_reward))

    def run(self):
        for episode in range(NUM_EPISODE):
            # algorithm 1: centralized allocator
            if self.alg == CENTRALIZED:
                # assign agent, starting from the highest reward patch
                for i in range(1, len(self.patches)):
                    for agent in self.patches[HOME].agents[:]: # copy
                        if self.patches[i].has_capacity(): 
                            self.patches[i].assign_agent(agent)
                            self.patches[HOME].remove_agent(agent)
            
            # algorithm 2: random
            # include home
            elif self.alg == RANDOM:
                for agent in self.patches[HOME].agents[:]: # note we are removing elements while iterating, use copy of array
                    patch_num = random.randint(0, len(self.patches) - 1)
                    self.patches[patch_num].assign_agent(agent)
                    self.patches[HOME].remove_agent(agent)
            
            # algorithm 3: choose which state to go to proportionally to its safety constraint; ignoring reward
            # include home
            elif self.alg == PROB:
                density = [] 
                for patch in self.patches:
                    density.append(1.0 * patch.cap_bound / self.num_agent)
                roulette_selector = roulette.Roulette(density)
                for agent in self.patches[HOME].agents[:]: # copy
                    action = roulette_selector.select()
                    self.patches[action].assign_agent(agent)
                    self.patches[HOME].remove_agent(agent)

            # algorithm 4: SC-MDP
            else:
                new_scmdp = scmdp.SCMDP()
                for agent in self.patches[HOME].agents[:]: # copy
                    action = new_scmdp.choose_act(state = HOME, T = 0)
                    self.patches[action].assign_agent(agent)
                    self.patches[HOME].remove_agent(agent)

            # detect violation
            for patch in self.patches:
                self.violation_count += patch.count_violation()

            # accumulate total reward
            for patch in self.patches:
                self.total_reward += patch.count_reward()

            self.print_patch_status()

            # all agents return home
            for i in range(1, len(self.patches)):
                self.patches[i].return_agents(self.patches[HOME])
            
            # each patch change bound except home
            for i in range(1, len(self.patches)):
                self.patches[i].change_bound()


new_exp = Experiment(num_agent = 1000, alg = PROB) # this would be 
new_exp.run()
