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
    g0.teeth_moved = 5
    gtrain.update()
    print("1) all gears OK, turning 5 teeth")
    assert (g0.angle, g0.broken) == (180, False)
    assert (g1.angle, g1.broken) == (90, False)
    assert (g2.angle, g2.broken) == (180, False)

    g0.angle = 0
    g1.angle = 0
    g2.angle = 0
    g0.teeth_moved = 5
    g1.broken = True
    gtrain.update()
    print("\n2) middle gear is broken, turning 5 teeth")
    assert (g0.angle, g0.broken) == (180, False)
    assert (g1.angle, g1.broken) == (0, True)
    assert (g2.angle, g2.broken) == (0, False)