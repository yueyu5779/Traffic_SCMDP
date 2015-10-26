"""
2D grid world simulation of traffic control
Experiment file
"""
from config import *
import world
import car

class Experiment:
    def __init__(self, vis = True):
        # initialize the world
        self.test_world = world.World()
        # initialize car
        self.cars = []
        for i in range(NUM_CARS):
            new_car = car.Car(start_pos = [0,0], dest_pos = [], world = self.test_world)
            self.cars.append(new_car)

        self.vis = vis
        if self.vis:
            self.test_world.draw(isNew = True)

    def run(self):
        while (True):
            self.cars[0].move(RIGHT) 
            
            if self.vis:
                self.test_world.window.getMouse()
                self.test_world.draw()
new_exp = Experiment()
new_exp.run()

raw_input("Please Press Enter to Exit")
        
