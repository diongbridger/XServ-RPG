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

    ## 1) all gears OK, turning 5 teeth
    g0.teeth_moved = 5
    gtrain.update()
    print()
    assert g0.angle  == 180
    assert g1.angle == 90
    assert g2.angle == 180

    ## 2) middle gear is broken, turning 5 teeth
    g0.angle = 0
    g1.angle = 0
    g2.angle = 0
    g0.teeth_moved = 5
    g1.broken = True
    gtrain.update()
    assert g0.angle == 180
    assert (g1.angle, g1.broken) == (0, True)
    assert g2.angle == 0
