'''experiment file'''

import world

NUM_PATCH = 10
REWARD = [10,9,8,7,6,5,4,3,2,1]
NUM_AGENT = 20
# capacity upper bound's upper limit
CAP_MAX_RAND = 50
NUM_EPISODE = 5
CENTRALIZED = True

class Experiment:
    def __init__(self):
        self.patches = []
        for i in range(NUM_PATCH):
            new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX_RAND)
            self.patches.append(new_patch)
        self.agents = []
        for i in range(NUM_AGENT):
            new_agent = world.Agent(identity = i)
            self.agents.append(new_agent)
        self.total_reward = 0
        self.violation_count = 0

    def run(self):
        for episode in range(NUM_EPISODE):
            # algorithm 1: centralized allocator
            if CENTRALIZED:
                # assign agent, starting from the highest reward patch
                for patch in self.patches:
                    for agent in self.agents[:]: # note we are removing elements while iterating, use copy of array
                        if patch.has_capacity(): 
                            patch.assign_agent(agent)
                            self.agents.remove(agent)
            
            # algorithm 2: SC-MDP
            else:
                pass
            # detect violation
            for patch in self.patches:
                self.violation_count += patch.count_violation()

            # accumulate total reward
            for patch in self.patches:
                self.total_reward += patch.count_reward()

            # status
            for patch in self.patches:
                print(patch.reward, patch.cap_bound, patch.cap_cur)

            # all agents return home
            for patch in self.patches:
                patch.return_agents(self.agents)
            
            # each patch change bound
            for patch in self.patches:
                patch.change_bound()

            print(self.violation_count, self.total_reward)

new_exp = Experiment()
new_exp.run()
