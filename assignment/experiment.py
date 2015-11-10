'''experiment file'''

import world
import random
import sys
import roulette
import scmdp
import numpy as np

NUM_STATE = 11
HOME = 0
REWARD = [0,10,9,8,7,6,5,4,3,2,1]

# capacity upper bound's upper limit
RAND_CAP = False
CAP_MAX_VALUE = 100
CAP_MAX = [CAP_MAX_VALUE for i in range(NUM_STATE - 1)] 
CAP_MAX.insert(0, 9999999) # home, its capacity is the number of agents
CAP_DENSITY = [1.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.9]

NUM_EPISODE = 3
# allocation algorithms
CENTRALIZED = 0
RANDOM = 1
PROB = 2
SCMDP = 3

DROP_RATIO = 0.0 # each episode each agent in nonhome patch has probability to be dropped
ADD_RATIO = 1.0 # each episode add some agents to home, but not exceeding initial total number

TRANS_SUC_RATE = 1.0 # state transition success rate

class Experiment:
    def __init__(self, num_agent, alg, trans_suc_rate, num_episode, num_state, data_file):
        # patch initialization
        self.patches = []
        self.num_state = num_state
        self.num_agent = num_agent

        # randomly generated capacities
        if RAND_CAP:
            for i in range(self.num_state):
                if i == 0: # home
                    new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX[i])
                    new_patch.cap_bound = self.num_agent
                else:
                    new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX[i])
                self.patches.append(new_patch)
        # predefined capacities
        else:
            for i in range(self.num_state):
                new_patch = world.Patch(identity = i, reward = REWARD[i], cap_max = CAP_MAX[i])
                new_patch.cap_bound = int(self.num_agent * CAP_DENSITY[i])
                self.patches.append(new_patch)

        # agent initialization
        for i in range(self.num_agent):
            new_agent = world.Agent(identity = i)
        # put all agents in patch0 (home)
            self.patches[HOME].assign_agent(new_agent)
        self.drop_count = 0 #count how many agents have been gone so far
        
        self.num_episode = num_episode
        self.alg = alg
        self.trans_suc_rate = trans_suc_rate
        
        #performance measurements
        self.violation_count = 0
        self.total_reward = 0

        self.data_file_name = data_file
        
    def print_patch_status(self):
            '''print status for all patches'''
            print("======================================")
            print("{:<12} {:<12} {:<12} {:<12} {:<12}".format("Reward", "Upperbound", "#agents", "Got Reward", "Violations"))
            for patch in self.patches:
                print("{:<12} {:<12} {:<12} {:<12} {:<12}".format(patch.reward, patch.cap_bound, patch.cap_cur, patch.cap_cur * patch.reward, patch.count_violation()))
            print("--------------------------------------")
            print("{:<12} {:<12} {:<12}".format("Violations", "Total Reward", "Total #agents"))
            print("{:<12} {:<12} {:<12}".format(self.violation_count, self.total_reward, self.num_agent - self.drop_count))
    
    def record_header(self):
        '''write experiment parameters to file'''
        self.data_file.write((str(self.num_agent) + ' '\
        + str(self.alg) + ' '\
        +str(self.trans_suc_rate)))

    def record(self, episode):
        '''write performance data to file'''
        self.data_file.write(episode)
        self.data_file.write(self.total_reward)
        self.data_file.wirte(self.violation_count)

    def run(self):
        self.data_file = open(self.data_file_name, 'w')
        self.record_header()
        for episode in range(self.num_episode - 1): # note: do not make decision at last step
            # algorithm 1: centralized allocator
            if self.alg == CENTRALIZED:
                # assign agent, starting from the highest reward patch
                for agent in self.patches[HOME].agents[:]: # copy
                    for i in range(1, len(self.patches)):
                        if self.patches[i].has_capacity():
                            if random.random() < self.trans_suc_rate: # transition 
                                self.patches[i].assign_agent(agent)
                                self.patches[HOME].remove_agent(agent)
                            break # note the break place: even transition did not success, do not assign this agent to another patch

            # algorithm 2: random
            # include home, all agents move uniformly random to another patch
            elif self.alg == RANDOM:
                # assignment step
                for patch in self.patches:
                    for agent in patch.agents: 
                        patch_num = random.randint(0, len(self.patches) - 1)
                        agent.assign_to(patch_num) 
                # actual move step
                for patch in self.patches:
                    for agent in patch.agents[:]: # copy 
                        if random.random() < self.trans_suc_rate: # transition:
                            self.patches[agent.assigned_patch].assign_agent(agent)
                            patch.remove_agent(agent)
            
            # algorithm 3: choose which state to go to proportionally to its safety constraint; ignoring reward
            elif self.alg == PROB:
                # solve for policy at the first episode
                if episode == 0: 
                    density = [] 
                    for patch in self.patches:
                        density.append(1.0 * patch.cap_bound / self.num_agent)
                    self.roulette_selector = roulette.Roulette(density)
                # assignment step
                for patch in self.patches:
                    for agent in patch.agents: 
                        patch_num = self.roulette_selector.select()
                        agent.assign_to(patch_num)
                # actual move step
                for patch in self.patches:
                    for agent in patch.agents[:]: #copy
                        if random.random() < self.trans_suc_rate: # transition:
                            self.patches[agent.assigned_patch].assign_agent(agent)
                            patch.remove_agent(agent)

            # algorithm 4: SC-MDP
            else:
                # solve for policy at the first episode
                if episode == 0:
                    # construct density, reward, initial distribution vector
                    density = [] 
                    rewards = []
                    initial_density = []
                    for patch in self.patches:
                        density.append(1.0 * patch.cap_bound / self.num_agent)
                        rewards.append(patch.reward)
                        initial_density.append(1.0 * patch.cap_cur / self.num_agent)
                    # initialize scmdp solver
                    self.scmdp_selector = scmdp.SCMDP(T = self.num_episode, n = self.num_state, A = self.num_state,\
                    trans_suc_rate = self.trans_suc_rate,\
                    reward_vec = rewards,\
                    cap_vec = density,\
                    x0 = initial_density)
                    self.scmdp_selector.solve()
                # assignment
                for patch in self.patches:
                    for agent in patch.agents: 
                        patch_num = self.scmdp_selector.choose_act(state = patch.identity, T = episode)
                        agent.assign_to(patch_num)
                # actual move step
                for patch in self.patches:
                    for agent in patch.agents[:]: #copy
                        if random.random() < self.trans_suc_rate: # transition:
                            self.patches[agent.assigned_patch].assign_agent(agent)
                            patch.remove_agent(agent)

            # detect violation
            for patch in self.patches:
                self.violation_count += patch.count_violation()

            # accumulate total reward
            for patch in self.patches:
                self.total_reward += patch.count_reward()
            
            # print experiment status of current episode
            self.print_patch_status()

            # Drop agents and add to home (except home)
            for i in range(1, len(self.patches)):
                for agent in self.patches[i].agents[:]: #copy
                    if random.random() < DROP_RATIO:
                        self.patches[i].remove_agent(agent)
                        self.drop_count += 1 

            # add some agents back to home (not the same number)
            max_num_add = self.drop_count
            for i in range(max_num_add):
                if random.random() < ADD_RATIO:
                    new_agent = world.Agent(identity = self.num_agent - self.drop_count)
                    # put all agents at home
                    self.patches[HOME].assign_agent(new_agent)
                    self.drop_count -= 1
        
        print("experiment finished")
        self.data_file.close()

new_exp = Experiment(num_agent = 100, alg = CENTRALIZED, \
trans_suc_rate = TRANS_SUC_RATE, \
num_episode = NUM_EPISODE, num_state = NUM_STATE,\
data_file = sys.argv[1]) 
new_exp.run()
