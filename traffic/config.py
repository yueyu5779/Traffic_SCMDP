import graphics as cg
import numpy
import random
import copy as cp

ROW = 0
COL = 1

# Enums for the map
INTERSECT = 0
ROAD = 1
OFFROAD = 2
# number of road blocks between 2 intersections
NUM_BLK_BTW = 3 
# The default car density
DEF_TRAFFIC = 0
# Map
CAP_MAX = 999
CAP_HZ_ROAD = [20, 30, 20, 10]
CAP_VT_ROAD = [30, 30, 20, 10]
# CONGEST_FACTOR = 1 if we want congest_prob to be 1.0 when current traffic is 200% capacity
# decrease this value to make penalty more harsh for violating upper bound 
CONGEST_FACTOR = 0.5 

# car actions
UP = 0; DOWN = 1; LEFT = 2; RIGHT = 3; STAY = 4
ACTIONS = [UP, DOWN, LEFT, RIGHT, STAY]

NUM_CARS = 20

# for visualization
CELL_SIZE = 50


