import numpy as np
from cvxopt import matrix, solvers
import gsc_mdp as GSC
import copy as cp
import roulette

np.set_printoptions(precision = 2, suppress = True)

class SCMDP:
    def __init__(self, reward_vec = [0, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1], \
    cap_vec = [1.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], \
    x0 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
        self.reward_vec = np.array(cp.deepcopy(reward_vec))
        self.cap_vec = np.array(cp.deepcopy(cap_vec))
        self.x0 = np.array(cp.deepcopy(x0))
        # length of planning horizon
        T = 2; self.T = T
        # number of states
        n = 11; self.n = n
        # number of actions
        A = 11; self.A = A
        # construct transition matrix G
        self.G = np.zeros((A, n, n))
        for act in range(A):
            # construct the 1-step transition matrix
            AG = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    # identity matrix
                    if i >= 1 and j >= 1 and i == j: AG[i][j] = 1
                    elif j == 0 and act == i: AG[i][j] = 1
            self.G[act,:,:] = cp.deepcopy(AG)
        # print(self.G)

        # construct reward matrix R (over T-1 horizon)
        self.R = np.zeros((T - 1, n, A))
        # stationary reward at t0
        R0 = np.zeros((n, A))
        for i in range(n):
            for j in range(A):
                R0[i][j] = self.reward_vec[i]
        for i in range(T-1):
            self.R[i,:,:] = R0
        # terminal reward at time T, a nx1 col vector
        self.RT = np.zeros((n, 1))
        for i in range(n):
            self.RT[i][0] = self.reward_vec[i]
        # print(self.R)
        # print(self.RT)

        # construct density vector
        self.d = self.cap_vec.reshape(len(self.cap_vec),1)
        # print(self.d)

        # construct L matrix
        self.L = np.eye(n)
        
        # initial distribution of the agents 
        self.x0 = self.x0.reshape(len(self.x0), 1)
        # print(self.x0)

        # discount factor
        self.gamma = 0.99

    def solve(self):
        [un_Q, un_x, phi_Q, phi_x, bf_Q, bf_x] = GSC.mdp(self.G, self.R, self.RT, self.L, self.d, self.x0, self.gamma)
        self.bf_Q = bf_Q
        print("Resulted bf policy:")
        print(self.bf_Q)
#        res_un = np.dot(self.d, np.ones((1, self.T))) - np.dot(self.L, un_x)
#        res_phi = np.dot(self.d, np.ones((1, self.T))) - np.dot(self.L, phi_x)
#        res_bf = np.dot(self.d, np.ones((1, self.T))) - np.dot(self.L, bf_x)
#        print(np.amin(res_un))
#        print(np.amin(res_phi))
#        print(np.amin(res_bf))
#        print(np.dot(self.L,un_x))
#        print(np.dot(self.L,phi_x))
#        print(np.dot(self.L,bf_x))

    def choose_act(self, state, T):
        policy = self.bf_Q[T][state]
        roulette_selector = roulette.Roulette(policy)
        action = roulette_selector.select()
        print("Action selected:", action)
        return action
        

sc = SCMDP()
sc.solve()
# sc.choose_act(state = 0, T = 0)
