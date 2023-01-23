#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
XServ Roguelike Version 0.1
Authors:
    - Dion Bridger
"""


from __future__ import annotations


from typing import Set
from typing import Optional

from abc import ABC as AbstractBaseClass
from abc import abstractmethod
from functools import lru_cache


class SimVariable:

    """
    """
    
    value: object

    def __init__(self, value, tags):
        self.value = value
        self.tags = tags ## "input", "output" or "internal"


class SimAtom(AbstractBaseClass):

    """
    SimAtom instances wrap sets of simulation state variables. They are the atomic components out of which complex simulations are assembled.
    The objects contained in internal and output variables should ONLY be change value if the `update` method is called.
    """

    ## ToDo:
    ##   - Write wrapper class that allows SimAtoms to negotiate a global update strategy using some number of feed-forward and feed-back operations.
    ##   - SimAtom to act as a facade for a target instance, where the facade.update() method may be simpler/faster than target.update() but have the
    ##   same input/output signature, so that target.update() will only be run if target.variables_internal is read out.

    variables: List[SimVariable]

    @lru_cache(1)
    def get_variables_input(self) -> Set[SimVariable]:
        return frozenset(filter(lambda v: "input" in v.tags, self.variables))

    @lru_cache(1)
    def get_variables_output(self) -> Set[SimVariable]:
        return frozenset(filter(lambda v: "output" in v.tags, self.variables))

    @lru_cache(1)
    def get_variables_internal(self) -> Set[SimVariable]:
        return frozenset(filter(lambda v: "internal" in v.tags, self.variables))

    @abstractmethod
    def update(self) -> None:
        """
        Update variables_output and variables_internal of the object to reflect changes to the input variables.
        Do NOT change any of the values in variables_input or change their state in any way.
        """
        pass


# class SimGraph:
#     @abstractmethod
#     def attach(self, other) -> Optional[SimAtom]:
#         """
#         Implementations should do exactly one of the following for any given value of `other`:
#         0. Return Optional.empty()
#         1. Return Optional.of(obj) where `obj` is a new SimAtom instance containing all of the variables belonging to both of the input objects.
#         """
#         pass




## ToDo: think through how SimAtom instances can be instantiated & deleted at run time. Should there be a special class to mediate this?
## ToDo: Seperate folder for examples 
## ToDo: Seperate folder for tests 

class Gear(SimAtom):

    def __init__(self, teeth):
        self.teeth = teeth
        self.angle = SimVariable(0, {"internal"})
        self.teeth_moved = SimVariable(0, {"input", "output"})
        self.variables = {self.teeth_moved, self.angle}

    def update(self):
        self.angle.value += (360*self.teeth_moved.value/self.teeth)%360


## This shouldn't exist, there has to be some way to compose individual gears to obtain this behaviour
class GearPair(SimAtom):
    
    def __init__(self, teeth):
        self.teeth = teeth
        self.angle = SimVariable(0, {"internal"})
        self.teeth_moved_0 = SimVariable(0, {"input", "output"})
        self.teeth_moved_1 = SimVariable(0, {"input", "output"})
        self.variables = {self.teeth_moved, self.angle}

    def update(self):
        angle_0 += (360*self.teeth_moved_0.value/self.teeth)%360
        angle_1 += (360*self.teeth_moved_1.value/self.teeth)%360
        self.teeth_moved_0.value = None
        self.teeth_moved_1.value = None
        ## Doesn't work. We need a flag to tell us which gear was turned.
        ## Back to the drawing board.
    


def gear_example():
    g1 = Gear(10)
    g2 = Gear(20)
    g3 = Gear(10)
    g1.teeth_moved.value = 5
    g1.update()
    print(g1.angle.value)
    g2.teeth_moved.value = g1.teeth_moved.value
    g2.update()
    print(g2.angle.value)
    g3.teeth_moved.value = g2.teeth_moved.value
    g3.update()
    print(g3.angle.value)


def main():
    gear_example()


if __name__ == "__main__":
    main()
