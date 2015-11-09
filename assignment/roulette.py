'''A roulette action selector'''

import random
import copy as cp
import numpy

class Roulette:
    ''' input: a weight vector, not necessarily normalized'''
    def __init__(self, weight):
        self.weight = cp.deepcopy(weight)
        self.num_actions = len(self.weight)
        #normalize, get probability for each action
        total_weight = 0
        for i in range(self.num_actions):
            total_weight += self.weight[i]
        for i in range(self.num_actions):
            self.weight[i] = 1.0 * self.weight[i] / total_weight

    def select(self):
        '''return an index that proportional to its probability'''
        #calc cumulative probability
        cum_prob = numpy.zeros(self.num_actions + 1)
        cum_prob[0] = 0
        for i in range(self.num_actions):
            cum_prob[i+1] = cum_prob[i] + self.weight[i]
        
        #random seed
        seed = random.random()
        for i in range(self.num_actions):
            if (seed >= cum_prob[i] and seed < cum_prob[i+1]):
                action = i

        return action


#roul = Roulette([2,4,4,10])
#count = numpy.zeros(roul.num_actions)
#for i in range(100000):
#    count[roul.select()] += 1
#print(count)
