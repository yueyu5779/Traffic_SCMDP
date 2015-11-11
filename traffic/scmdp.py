import numpy as np
from cvxopt import matrix, solvers
import gsc_mdp as GSC
import copy as cp
import roulette

from config import *
import world
import car
import state

np.set_printoptions(precision = 2, suppress = True, threshold = 'nan')

class SCMDP:
    def __init__(self, T, n, A, m, trans_suc_rate):
        # length of planning horizon
        self.T = T
        # number of states
        self.n = n
        # number of actions
        self.A = A
        # number of constraints
        self.m = m
        
        # construct transition matrix G
        self.trans_suc_rate = trans_suc_rate
        self.G = self.construct_G()  
        # print(self.G)

        # construct reward matrix R (over T-1 horizon)
        self.RT = self.construct_RT() 
        self.R = self.construct_R()
        # print(self.R)
        # print(self.RT)

        # construct density vector
        self.d = self.construct_d()
        # print(self.d)

        # construct L matrix
        self.L = self.construct_L()
        
        # initial distribution of the agents 
        self.x0 = self.construct_x0()
        # print(self.x0)

        # discount factor
        self.gamma = 0.99
        
        # policy matrix
        self.bf_Q = []
        self.bf_x = []
        self.phi_Q = []
        self.phi_x = []
        self.un_Q = []
        self.un_x = []

    def construct_G(self):
        '''A x n x n'''
        pass

    def construct_RT(self):
        ''' n x 1'''
        pass

    def construct_R(self):
        ''' (T-1) x n x A'''
        pass

    def construct_L(self):
        ''' m x n'''
        pass

    def construct_d(self):
        ''' m x 1'''
        pass

    def construct_x0(self):
        ''' n x 1, assume cars are distributed equally in each corner; so 1/8 of each type at each corner '''
        pass


    def solve(self):
        [self.un_Q, self.un_x, self.phi_Q, self.phi_x, self.bf_Q, self.bf_x] = GSC.mdp(self.G, self.R, self.RT, self.L, self.d, self.x0, self.gamma)
        print("scmdp policy solved")
#        print(self.bf_Q)
#        print(bf_x)
#        res_un = np.dot(self.d, np.ones((1, self.T))) - np.dot(self.L, un_x)
#        res_phi = np.dot(self.d, np.ones((1, self.T))) - np.dot(self.L, phi_x)
#        res_bf = np.dot(self.d, np.ones((1, self.T))) - np.dot(self.L, bf_x)
#        print(np.amin(res_un))
#        print(np.amin(res_phi))
#        print(np.amin(res_bf))
#        print(np.dot(self.L,un_x))
#        print(np.dot(self.L,phi_x))
#        print(np.dot(self.L,bf_x))

    def save_to_file(self):
        '''save un_Q, un_x, phi_Q, phi_x, bf_Q, bf_x to .npy files'''
        pass

    def load_from_file(self):
        pass

    def choose_act(self, state, T):
        policy = self.bf_Q[T][state]
        # print("Policy vector", policy)
        roulette_selector = roulette.Roulette(policy)
        action = roulette_selector.select()
        # print("Action selected:", action)
        return action

    def choose_act_phi(self, state, T):
        policy = self.phi_Q[T][state]
        # print("Policy vector", policy)
        roulette_selector = roulette.Roulette(policy)
        action = roulette_selector.select()
        # print("Action selected:", action)
        return action

if __name__ == "__main__":
    # call solve and store resulted matrices
    test_world = world.World()
    state_dict = state.StateDict(test_world) 
    scmdp_solver = SCMDP(T = 15, m = test_world.num_road,  n = state_dict.num_state, A = len(ACTIONS), trans_suc_rate = TRANS_SUC_RATE)
    #scmdp_solver.solve()
    #scmdp_solver.save_to_file()
