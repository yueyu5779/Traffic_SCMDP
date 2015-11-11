import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import copy as cp
import scipy.stats as ss

NUM_EXP = 50
dirname = "data_5/"

def process_file(filename):
    data_file = open(filename, 'r')
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
    data_file.close()
    return episodes, rewards, violations

def process_data(name):
    eps = []
    rs = []
    vs = []

    for i in range(NUM_EXP):
        filename = dirname + name + str(i) + ".data"
        eps_, rs_, vs_ = process_file(filename)
        eps.append(cp.deepcopy(eps_))
        rs.append(cp.deepcopy(rs_))
        vs.append(cp.deepcopy(vs_))
    
    eps = np.array(eps) 
    rs = np.array(rs)
    vs = np.array(vs)
    rs_mean = np.mean(rs, axis = 0)
    rs_std = np.std(rs, axis = 0)
    vs_mean = np.mean(vs, axis = 0)
    vs_std = np.std(vs, axis = 0)
    dof = np.empty(len(eps[0]))
    dof.fill(NUM_EXP)

    return dof, eps, rs_mean, rs_std, vs_mean, vs_std

SHOW_REWARD = True
cent_dof, cent_eps, cent_rs_mean, cent_rs_std, cent_vs_mean, cent_vs_std = process_data("CENTRALIZED")
rand_dof, rand_eps, rand_rs_mean, rand_rs_std, rand_vs_mean, rand_vs_std = process_data("RANDOM")
safe_dof, safe_eps, safe_rs_mean, safe_rs_std, safe_vs_mean, safe_vs_std = process_data("SAFE")
grdy_dof, grdy_eps, grdy_rs_mean, grdy_rs_std, grdy_vs_mean, grdy_vs_std = process_data("GREEDY")
smdpphi_dof, smdpphi_eps, smdpphi_rs_mean, smdpphi_rs_std, smdpphi_vs_mean, smdpphi_vs_std = process_data("SCMDPPHI")
smdpbf_dof, smdpbf_eps, smdpbf_rs_mean, smdpbf_rs_std, smdpbf_vs_mean, smdpbf_vs_std = process_data("SCMDPBF")

if SHOW_REWARD:
    # plot rewards
    plt.errorbar(cent_eps[0], cent_rs_mean, yerr=ss.t.ppf(0.95, cent_dof)*cent_rs_std, color = 'c')
    plt.errorbar(rand_eps[0], rand_rs_mean, yerr=ss.t.ppf(0.95, rand_dof)*rand_rs_std, color = 'k')
    plt.errorbar(safe_eps[0], safe_rs_mean, yerr=ss.t.ppf(0.95, safe_dof)*safe_rs_std, color = 'y')
    plt.errorbar(grdy_eps[0], grdy_rs_mean, yerr=ss.t.ppf(0.95, grdy_dof)*grdy_rs_std, color = 'g')
    plt.errorbar(smdpphi_eps[0], smdpphi_rs_mean, yerr=ss.t.ppf(0.95, smdpphi_dof)*smdpphi_rs_std, color = 'r')
    plt.errorbar(smdpbf_eps[0], smdpbf_rs_mean, yerr=ss.t.ppf(0.95, smdpbf_dof)*smdpbf_rs_std, color = 'b')
#    plt.xlim((-1,100))
    plt.show()

#else:
# plot violations
    plt.errorbar(cent_eps[0], cent_vs_mean, yerr=ss.t.ppf(0.95, cent_dof)*cent_vs_std, color = 'c')
    plt.errorbar(rand_eps[0], rand_vs_mean, yerr=ss.t.ppf(0.95, rand_dof)*rand_vs_std, color = 'k')
    plt.errorbar(safe_eps[0], safe_vs_mean, yerr=ss.t.ppf(0.95, safe_dof)*safe_vs_std, color = 'y')
    plt.errorbar(grdy_eps[0], grdy_vs_mean, yerr=ss.t.ppf(0.95, grdy_dof)*grdy_vs_std, color = 'g')
    plt.errorbar(smdpphi_eps[0], smdpphi_vs_mean, yerr=ss.t.ppf(0.95, smdpphi_dof)*smdpphi_vs_std, color = 'r')
    plt.errorbar(smdpbf_eps[0], smdpbf_vs_mean, yerr=ss.t.ppf(0.95, smdpbf_dof)*smdpbf_vs_std, color = 'b')
    #plt.yscale("log") #,linthreshy=100)
#    ax.set_yscale("log")
    plt.show()


