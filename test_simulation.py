#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from gears import Gear, GearTrain
# codify gear example into a test

def test_geartrain_implementation_in_simnode():
    g0 = Gear(10)
    g1 = Gear(20)
    g2 = Gear(10)
    gtrain = GearTrain(g0)
    gtrain.add_gear(g1)
    gtrain.add_gear(g2)

    ## 1) All gears OK, turning 5 teeth.
    g0.teeth_moved = 5
    gtrain.update()
    print()
    assert (g0.angle, g0.direction) == (180,  1)
    assert (g1.angle, g1.direction) == (-90, -1)
    assert (g2.angle, g2.direction) == (180,  1)

    ## 2) Middle gear is broken, turning 5 teeth.
    g0.angle = 0
    g1.angle = 0
    g2.angle = 0
    g0.direction = 1
    g1.direction = 1
    g2.direction = 1
    g0.teeth_moved = 5
    g1.broken = True
    gtrain.update()
    assert (g0.angle, g0.direction, g0.broken) == (180, 1, False)
    assert (g1.angle, g1.direction, g1.broken) == (0,  -1, True)  
    assert (g2.angle, g2.direction, g2.broken) == (0,   1, False) ## gear should not break if turned by 0 teeth.
    ## notice direction switched even though g1 did not rotate, since direction is an input variable rather than a state variable
