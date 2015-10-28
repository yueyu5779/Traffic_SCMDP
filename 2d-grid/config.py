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
NUM_BLK_BTW = 1 
# The default car density
DEF_TRAFFIC = 0
# Map
CAP_MAX = 999
CAP_HZ_ROAD = [10,20,6]
CAP_VT_ROAD = [8,14,24]

# car actions
UP = 0; DOWN = 1; LEFT = 2; RIGHT = 3; STAY = 4
ACTIONS = [UP, DOWN, LEFT, RIGHT, STAY]

NUM_CARS = 1

# for visualization
CELL_SIZE = 80


