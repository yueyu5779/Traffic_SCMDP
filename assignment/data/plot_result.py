import pylab
import sys
import re
import numpy as np
import matplotlib.pyplot as plt

def process_file(data_file):
    episodes = []
    rewards = []
    violations = []
    line_count = 0
    for line in data_file:
        if line_count != 0:
            data = re.split(',|\n', line)
            episodes.append(float(data[0]))
            rewards.append(float(data[1]))
            violations.append(float(data[2]))
        line_count += 1
    return episodes, rewards, violations

rand_data_file = open("rand.txt", 'r')
rand_e, rand_r, rand_v = process_file(rand_data_file)
rand_data_file = open("rand.txt", 'r')
rand_data_file = open("rand.txt", 'r')
rand_data_file = open("rand.txt", 'r')

# red dashes, blue squares and green triangles
plt.plot(rand_e, rand_v, 'r--')
plt.show()

def plot_reward():
    pass
