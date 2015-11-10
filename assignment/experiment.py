'''experiment file'''

import world
import random
import sys
import roulette
import scmdp
import numpy as np

NUM_AGENT = 1000
NUM_STATE = 11
HOME = 0
REWARD = [0,1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]

# capacity density upper bound
CAP_DENSITY = [1.0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
#CAP_DENSITY = [1.0, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

NUM_EPISODE = 20
# allocation algorithms
CENTRALIZED = 0
RANDOM = 1
SAFE = 2
GREEDY = 3
SCMDP = 4
ALGS = [CENTRALIZED, RANDOM, SAFE, GREEDY, SCMDP]
ALGS_NAME = ["CENTRALIZED", "RANDOM", "SAFE", "GREEDY", "SCMDP"]

DROP_RATIO = 0.5 # each episode each agent in nonhome patch has probability to be dropped
ADD_RATIO = 0.75 # each episode add some agents to home, but not exceeding initial total number

TRANS_SUC_RATE = 0.9 # state transition success rate

class Experiment:
    def __init__(self, num_agent, alg, trans_suc_rate, num_episode, num_state, drop_ratio, add_ratio, rewards, cap_density, data_file):
        # patch initialization
        self.patches = []
        self.num_state = num_state
        self.num_agent = num_agent
        self.rewards = rewards
        self.cap_density = cap_density

        # randomly generated capacities
        for i in range(self.num_state):
            new_patch = world.Patch(identity = i, reward = self.rewards[i], cap_bound = int(self.cap_density[i] * self.num_agent))
            self.patches.append(new_patch)

        # agent initialization
        for i in range(self.num_agent):
            new_agent = world.Agent(identity = i)
            self.patches[HOME].assign_agent(new_agent)
        
        self.drop_count = 0 # count how many agents have been dropped so far
        self.drop_ratio = drop_ratio
        self.add_ratio = add_ratio
        self.num_episode = num_episode
        self.alg = alg
        self.trans_suc_rate = trans_suc_rate
        
        # performance measurements
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
        self.data_file.write(\
        "num_agent: " + str(self.num_agent) + ' '\
        + "algorithm: "+ ALGS_NAME[self.alg] + ' '\
        + "trans_suc_rate: " + str(self.trans_suc_rate) + ' '\
        + "num_episode: " + str(self.num_episode) + ' '\
        + "num_state: " + str(self.num_state) + ' '\
        + "rewards: " + str(REWARD) + ' '\
        + "density: " + str(CAP_DENSITY) + ' '\
        + "drop_ratio: " + str(self.drop_ratio) + ' '\
        + "add_ratio: " + str(self.add_ratio) + '\n')

    def record(self, episode):
        '''write performance data to file'''
        self.data_file.write(str(episode) + ',')
        self.data_file.write(str(self.total_reward) + ',')
        self.data_file.write(str(self.violation_count))
        self.data_file.write('\n')
        
    def move_agents(self):
        ''' call after assignment, move all agents to their assigned destinations'''
        for patch in self.patches:
            for agent in patch.agents[:]: #copy
                if random.random() < self.trans_suc_rate: # transition:
                    self.patches[agent.assigned_patch].assign_agent(agent)
                    patch.remove_agent(agent)

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
                self.move_agents()

            # algorithm 3: choose which state to go to proportionally to its safety constraint; ignoring reward
            elif self.alg == SAFE:
                # solve for policy at the first episode
                if episode == 0: 
                    self.roulette_selector = roulette.Roulette(self.cap_density)
                # assignment step
                for patch in self.patches:
                    for agent in patch.agents: 
                        patch_num = self.roulette_selector.select()
                        agent.assign_to(patch_num)
                # actual move step
                self.move_agents()
            
            # algorithm 4: choose which state to go to proportionally to its reward; ignore safety
            elif self.alg == GREEDY:
                # solve for policy at the first episode
                if episode == 0: 
                    self.roulette_selector = roulette.Roulette(self.rewards)
                # assignment step
                for patch in self.patches:
                    for agent in patch.agents: 
                        patch_num = self.roulette_selector.select()
                        agent.assign_to(patch_num)
                # actual move step
                self.move_agents()

            # algorithm 4: SC-MDP
            elif self.alg == SCMDP:
                # solve for policy at the first episode
                if episode == 0:
                    # construct density, reward, initial distribution vector
                    initial_density = []
                    for patch in self.patches:
                        initial_density.append(1.0 * patch.cap_cur / self.num_agent)
                    # initialize scmdp solver
                    self.scmdp_selector = scmdp.SCMDP(T = self.num_episode, n = self.num_state, A = self.num_state,\
                    trans_suc_rate = self.trans_suc_rate, reward_vec = self.rewards, cap_vec = self.cap_density, x0 = initial_density)
                    # solve for policy matrix
                    self.scmdp_selector.solve()
                # assignment
                for patch in self.patches:
                    for agent in patch.agents: 
                        patch_num = self.scmdp_selector.choose_act(state = patch.identity, T = agent.clock)
                        agent.assign_to(patch_num)
                        agent.tick() # important: time clock counts
                # actual move step
                self.move_agents()

            # detect violation
            for patch in self.patches:
                self.violation_count += patch.count_violation()

            # accumulate total reward
            for patch in self.patches:
                self.total_reward += patch.count_reward()
            
            # print experiment status of current episode
            # self.print_patch_status()
            self.record(episode)

            # Drop agents and add to home (except home)
            for i in range(1, len(self.patches)):
                for agent in self.patches[i].agents[:]: #copy
                    if random.random() < self.drop_ratio:
                        self.patches[i].remove_agent(agent)
                        self.drop_count += 1 

            # add some agents back to home (not the same number)
            max_num_add = self.drop_count
            for i in range(max_num_add):
                if random.random() < self.add_ratio:
                    new_agent = world.Agent(identity = self.num_agent - self.drop_count)
                    # put all agents at home
                    self.patches[HOME].assign_agent(new_agent)
                    self.drop_count -= 1
        
        print("experiment finished")
        self.data_file.close()


for i in range(len(ALGS)):
    new_exp = Experiment(num_agent = NUM_AGENT, alg = ALGS[i],\
    trans_suc_rate = TRANS_SUC_RATE,\
    num_episode = NUM_EPISODE, num_state = NUM_STATE,\
    drop_ratio = DROP_RATIO, add_ratio = ADD_RATIO,\
    rewards = REWARD, cap_density = CAP_DENSITY,\
    data_file = "data/" + ALGS_NAME[i] + ".data") 
    new_exp.run()
