#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from gears import Gear, GearTrain
# codify gear example into a test

def test_geartrain_implementation_in_simnode():
    g0 = Gear(10)
    g1 = Gear(20)
    g2 = Gear(10)

    ## eliminate chance so test is repeatable
    g0.probability_of_breaking_per_tooth_click = 0
    g1.probability_of_breaking_per_tooth_click = 0
    g2.probability_of_breaking_per_tooth_click = 0

    # make a gear train
    gtrain = GearTrain()
    gtrain.add_gear(g0)
    gtrain.add_gear(g1)
    gtrain.add_gear(g2)

    ## 1) All gears OK, turning 5 teeth.
    gtrain.teeth_moved = 5
    gtrain.update()
    assert (g0.angle, g0.direction, g0.broken) == (180,  1, False)
    assert (g1.angle, g1.direction, g1.broken) == (-90, -1, False)
    assert (g2.angle, g2.direction, g2.broken) == (180,  1, False)

    ## 2) Middle gear is broken, turning 5 teeth.
    g0.angle = 0
    g1.angle = 0
    g2.angle = 0
    g0.direction = 1
    g1.direction = 1
    g2.direction = 1
    g0.teeth_moved = 5
    g1.probability_of_breaking_per_tooth_click = 1

    ## save state variables for comparison
    g1_state_before = g1.get_state_variables()
    g1_input_before = g1.get_input_variables()
    g2_state_before = g2.get_state_variables()
    g2_input_before = g2.get_input_variables()

    assert gtrain.update()
    assert (g0.angle, g0.direction, g0.broken) == (180, 1, False)
    assert (g1.angle, g1.direction, g1.broken) == (0,  -1, True)  
    assert (g2.angle, g2.direction, g2.broken) == (0,   1, False) ## gear should not break if turned by 0 teeth.

    ## causal chain broken by g1, g2 should be unaffected
    assert g1.get_state_variables() != g1_state_before ## g1 broke, but
    assert g1.get_input_variables() != g1_input_before ## g1 update was attempted
    assert g2.get_state_variables() == g2_state_before
    assert g2.get_input_variables() == g2_input_before
    ## notice direction switched even though g1 did not rotate, since direction is an input variable rather than a state variable
