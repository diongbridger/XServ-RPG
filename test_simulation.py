#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from gears import Gear, GearTrain
# separate tests for readability
# arrange, act, assert

@pytest.fixture
def gear1():
    gear = Gear(10)
    gear.probability_of_breaking_per_tooth_click = 0 # NDH: having to move this into declaration feels like anti pattern
    return gear

@pytest.fixture
def gear2():
    gear = Gear(20)
    gear.probability_of_breaking_per_tooth_click = 0
    return gear

@pytest.fixture
def gear3():
    gear = Gear(10)
    gear.probability_of_breaking_per_tooth_click = 0
    return gear

@pytest.fixture
def gear_train(gear1, gear2, gear3):
    gtrain = GearTrain()
    gtrain.add_gear(gear1)
    gtrain.add_gear(gear2)
    gtrain.add_gear(gear3) # NDH: i think this reveals we should add a *args to the aggregate constructors or otherwise abstract GearTrains representation
    return gtrain

def test_geartrain_implementation_in_simnode(gear1, gear2, gear3, gear_train):
    # NDH: I had to keep these two lines up here or this test would fail for some reason
    gear_train.teeth_moved = 5
    gear_train.update()


    ## 2) Middle gear is broken, turning 5 teeth.
    gear1.angle = 0
    gear2.angle = 0
    gear3.angle = 0
    gear1.direction = 1
    gear2.direction = 1
    gear3.direction = 1
    gear1.teeth_moved = 5
    gear2.probability_of_breaking_per_tooth_click = 1

    ## save state variables for comparison
    gear2_state_before = gear2.get_state_variables()
    gear2_input_before = gear2.get_input_variables()
    gear3_state_before = gear3.get_state_variables()
    gear3_input_before = gear3.get_input_variables()

    assert gear_train.update()
    # NDH: I see in the implementation update this returns False if unsuccessful.
    # It's more pythonic to define an exception "UpdateException" that can be thrown from those classes.
    # That way we can catch it where we need to without doing boolean compares. This is especially useful when we start working with try catch game loop.

    assert (gear1.angle, gear1.direction, gear1.broken) == (180, 1, False)
    assert (gear2.angle, gear2.direction, gear2.broken) == (0,  -1, True)
    assert (gear3.angle, gear3.direction, gear3.broken) == (0,   1, False) ## gear should not break if turned by 0 teeth.

    ## causal chain broken by gear2, gear3 should be unaffected
    assert gear2.get_state_variables() != gear2_state_before ## gear2 broke, but
    assert gear2.get_input_variables() != gear2_input_before ## gear2 update was attempted
    assert gear3.get_state_variables() == gear3_state_before
    assert gear3.get_input_variables() == gear3_input_before
    ## notice direction switched even though gear2 did not rotate, since direction is an input variable rather than a state variable

def test_gears_turn_then_update_angle_and_direction(gear1, gear2, gear3, gear_train): #NDH: code duplication in test signature means I should probably group these
    ## 1) All gears OK, turning 5 teeth.
    gear_train.teeth_moved = 5
    gear_train.update()
    assert (gear1.angle, gear1.direction, gear1.broken) == (180,  1, False)
    assert (gear2.angle, gear2.direction, gear2.broken) == (-90, -1, False)
    assert (gear3.angle, gear3.direction, gear3.broken) == (180,  1, False)