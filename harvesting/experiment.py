'''experiment file'''

import world
import random
import sys

NUM_PATCH = 10
REWARD = [10,9,8,7,6,5,4,3,2,1]
NUM_AGENT = 20
# capacity upper bound's upper limit
CAP_MAX_RAND = 10
NUM_EPISODE = 2

# allocation algorithms
CENTRALIZED = 0
RANDOM = 1
SCMDP = 2
ALG = RANDOM

class Experiment:
    def __init__(self, num_agent = NUM_AGENT, alg = ALG):
        self.patches = []
        for i in range(NUM_PATCH):
            new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX_RAND)
            self.patches.append(new_patch)
        self.agents = []
        self.num_agent = num_agent
        for i in range(self.num_agent):
            new_agent = world.Agent(identity = i)
            self.agents.append(new_agent)
        self.total_reward = 0
        self.violation_count = 0
        self.alg = alg

    def print_patch_status(self):
            '''print status for all patches'''
            print("======================================")
            print("{:<12} {:<12} {:<12}".format("Reward", "Upperbound", "#agents"))
            for patch in self.patches:
                print("{:<12} {:<12} {:<12}".format(patch.reward, patch.cap_bound, patch.cap_cur))
            print("--------------------------------------")
            print("{:<12} {:<12}".format("Volations", "Total Reward"))
            print("{:<12} {:<12}".format(self.violation_count,self.total_reward))

    def run(self):
        for episode in range(NUM_EPISODE):
            # algorithm 1: centralized allocator
            if self.alg == CENTRALIZED:
                # assign agent, starting from the highest reward patch
                for patch in self.patches:
                    for agent in self.agents[:]: # note we are removing elements while iterating, use copy of array
                        if patch.has_capacity(): 
                            patch.assign_agent(agent)
                            self.agents.remove(agent)
            
            # algorithm 2: random
            elif self.alg == RANDOM:
                for agent in self.agents[:]: # note we are removing elements while iterating, use copy of array
                    patch = random.choice(self.patches)
                    patch.assign_agent(agent)
                    self.agents.remove(agent)
            
            # algorithm 3: SC-MDP
            else:
                pass

            # detect violation
            for patch in self.patches:
                self.violation_count += patch.count_violation()

            # accumulate total reward
            for patch in self.patches:
                self.total_reward += patch.count_reward()

            self.print_patch_status()

            # all agents return home
            for patch in self.patches:
                patch.return_agents(self.agents)
            
            # each patch change bound
            for patch in self.patches:
                patch.change_bound()


new_exp = Experiment(num_agent = 50, alg = RANDOM) # this would be 
new_exp.run()
