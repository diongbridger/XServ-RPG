#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from simulation import SimNode, SimGraph, SimArrow

class Gear(SimNode):

    def __init__(self, teeth):

        ## static parameters
        self.teeth = teeth

        ## variables
        self.angle = 0
        self.teeth_moved = 0
        self.direction = 1 ## 1=clockwise. -1=anticlockwise
        self.broken = False
        self.probability_of_breaking_per_tooth_click = 0 ## default 0 so as not to mess with unit tests

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
        if angle < 0:
            angle += 360
        self.angle = angle
        return True


class GearPair(SimArrow):

    def __init__(self, source:Gear, target:Gear):
        self.source = source
        self.target = target

    def effect(self) -> bool:
        if not self.source.broken:
            self.target.direction = -1*self.source.direction
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
