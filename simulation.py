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
    They are the nodeic components out of which complex simulations are assembled.
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


class SimGraph(AbstractBaseClass):

    """
    A SimGraph is composed of a set of connected SimArrow instances, and may include cycles. If the graph includes cycles then the causal chain will stop
    once chain of atom updates comes back around to the first atom updated.
    """

    pass



## ############## ##
## ## Examples ## ##
## ############## ##

# ToDo:
#   - move examples into a separate file.
#   - think through how to model causal graphs with closed loops. E.g. gears arranged in a ring.