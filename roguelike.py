#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
XServ Roguelike Version 0.1
Authors:
    - Dion Bridger
"""


import random


from abc import ABC as AbstractBaseClass
from abc import abstractmethod


class SimNode(AbstractBaseClass):
    
    """
    SimNode instances wrap sets of simulation state variables.
    They are the most fine-grained components out of which complex simulations are assembled.
    """
    
    @abstractmethod
    def update(self) -> bool:
        """
        When a SimNode's update() method is called, some of the variables belonging to the node can be updated to reflect changes made to its
        input variables.
        """
        pass


class SimArrow(AbstractBaseClass):
    
    """
    Arrows represent unidirection causal relationships between nodes.
    All arrows must implement an 'effect' which copies values from the source to the target.
    """
    
    source: SimNode
    target: SimNode

    def update(self) -> bool:
        if self.effect():
            return self.target.update()
        return False

    @abstractmethod
    def effect(self) -> bool:
        """
        The effect method should implement the causal relationship represented by the arrow. This means copying the value of at least one of the variables
        of the source node into a variable in the target node, but not vice versa.
        """
        pass


class SimGraph:

    """
    A SimGraph is composed of a set of connected SimArrow instances, and may include cycles. If the graph includes cycles then the causal chain will stop
    once chain of atom updates comes back around to the first atom updated.
    """

    ## Status: stub class
    ## ToDo: 
    ##   - cycle checking
    ##   - conflict / deadlock checking (consider three gears all connected, none should be able to actually turn)
    ##   - "intelligent" arrow updates, don't update down a dead causal chain

    def __init__(self):
        self.arrows = list()

    def add_arrow(self, arrow:SimArrow):
        self.arrows.append(arrow)

    def update(self) -> bool:
        for a in self.arrows:
            a.update()


  ## ############## ##
 ## ## Examples ## ##
## ############## ##

# ToDo:
#   - move examples into a separate file.
#   - think through how to model causal graphs with closed loops. E.g. gears arranged in a ring.

class Gear(SimNode):
    
    def __init__(self, teeth):
        
        ## static parameters
        self.teeth = teeth
        
        ## variables
        self.angle = 0
        self.teeth_moved = 0
        self.broken = False
        self.probability_of_breaking_per_tooth_click = 1/100
    
    def update(self) -> bool:
        if self.broken:
            return False
        teeth_moved = 0
        for i in range(self.teeth_moved):
            self.broken = random.random() < self.probability_of_breaking_per_tooth_click 
            if self.broken:
                break
            teeth_moved += 1
        self.teeth_moved = teeth_moved
        self.angle = (360*teeth_moved/self.teeth)%360
        return True


class GearPair(SimArrow):

    def __init__(self, source:Gear, target:Gear):
        self.source = source
        self.target = target

    def effect(self) -> bool:
        if not self.source.broken:
            self.target.teeth_moved = self.source.teeth_moved
            return True
        return False


class GearTrain(SimNode):
    
    def __init__(self, start_gear:Gear):
        self.teeth_moved = 0
        self.gears = [start_gear,]
        self.arrows = []
    
    def add_gear(self, gear):
        self.arrows.append(GearPair(self.gears[-1], gear))
        self.gears.append(gear)
    
    def update(self):
        self.gears[0].update()
        for a in self.arrows:
            if not a.update():
                break


def gear_example():
    g0 = Gear(10)
    g1 = Gear(20)
    g2 = Gear(10)
    gtrain = GearTrain(g0)
    gtrain.add_gear(g1)
    gtrain.add_gear(g2)
    g0.teeth_moved = 5
    gtrain.update()
    print("1) all gears OK, turning 5 teeth")
    print(g0.angle, g0.broken)
    print(g1.angle, g1.broken)
    print(g2.angle, g2.broken)

    g0.angle = 0
    g1.angle = 0
    g2.angle = 0
    g0.teeth_moved = 5
    g1.broken = True
    gtrain.update()
    print("\n2) middle gear is broken, turning 5 teeth")
    print(g0.angle, g0.broken)
    print(g1.angle, g1.broken)
    print(g2.angle, g2.broken)
    

if __name__ == "__main__":
    main()
