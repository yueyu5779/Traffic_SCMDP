"""
2D grid world simulation of traffic control
Experiment file
"""
from config import *
import world
import car

GREEDY = 0 # Shortest path
A_STAR = 1
SCMDP = 2

class Experiment:
    def __init__(self, vis = True, alg = GREEDY):
        # initialize the world
        self.test_world = world.World()
        # initialize car
        self.cars = []
        for i in range(NUM_CARS):
            new_car = car.Car(identity = i, start = [0,0], dest = [12,12], world = self.test_world, car_type = SMALL)
            self.cars.append(new_car)
        
        self.alg = alg

        self.vis = vis
        if self.vis:
            self.test_world.draw(isNew = True)

    def run(self):
        while (True):
            # visualization
            if self.vis:
                print("==========================================================")
                print("{:<6} {:<6} {:<6}".format("CarID", "Position", "Destination"))
                for car in self.cars:
                    car.print_status()
                self.test_world.draw()
                self.test_world.window.getMouse()
            
            for car in self.cars: 
                if self.alg == GREEDY:             
                    car.greedy_act() 
            
new_exp = Experiment(alg = GREEDY)
new_exp.run()

raw_input("Please Press Enter to Exit")
        
