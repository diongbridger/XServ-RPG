#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from simulation import SimNode, SimGraph, SimArrow

class Gear(SimNode):

    instance_number = 0

    def __init__(self, teeth):
        self.instance_number = Gear.instance_number
        Gear.instance_number += 1

        ## static parameters
        self.teeth = teeth

        ## variables
        self.angle = 0 ## should be in the range [-180,180]
        self.teeth_moved = 0
        self.direction = 1 ## 1=clockwise. -1=anticlockwise
        self.broken = False
        self.probability_of_breaking_per_tooth_click = 0 ## default 0 so as not to mess with unit tests

    def __repr__(self):
        return f"Gear[{self.instance_number}]"

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
        angle_delta = self.direction*(360*teeth_moved/self.teeth)
        angle = (self.angle+angle_delta)%360
        if 180 < angle:
            angle += -360
        elif angle < -180:
            angle += 360
        self.angle = angle
        return True

    def get_state_variables(self) -> dict:
        return {
            "angle": self.angle,
            "broken": self.broken,
            "probability_of_breaking_per_tooth_click": self.probability_of_breaking_per_tooth_click
        }

    def get_input_variables(self) -> dict:
        return {
            "direction": self.direction,
            "teeth_moved": self.teeth_moved,
        }


class GearPair(SimArrow):

    def __init__(self, source:Gear, target:Gear):
        self.source = source
        self.target = target

    def __repr__(self):
        return f"GearPair[{self.source.instance_number}, {self.target.instance_number}]"

    def effect(self) -> bool:
        if not self.source.broken:
            self.target.direction = -1*self.source.direction
            self.target.teeth_moved = self.source.teeth_moved
            return True
        return False


class GearTrain:

    def __init__(self):
        self.gears = list()
        self.teeth_moved = 0
        self.sim_graph = SimGraph()

    def add_gear(self, gear):
        self.gears.append(gear)
        if 2<=len(self.gears):
            gp = GearPair(self.gears[-2], self.gears[-1])
            self.sim_graph.add_arrow(gp)

    def update(self):
        self.gears[0].teeth_moved = self.teeth_moved
        return self.sim_graph.update()
