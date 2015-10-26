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
CAP_HZ_ROAD = [20, 30, 40, 20]
CAP_VT_ROAD = [50, 20, 30, 30]

# car actions
UP = 0; DOWN = 1; LEFT = 2; RIGHT = 3

NUM_CARS = 1



