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

from collections import defaultdict

# ToDo:
#   - move examples into a separate file.
#   - think through how to model causal graphs with closed loops. E.g. gears arranged in a ring.


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

    @abstractmethod
    def get_state_variables(self) -> dict:
        """
        Get a dictionary containing all the state variables of the SimNode. This can be used to check whether the state of a node was altered without
        having to check the individual member variables of the node, or even having to know what they actually are.
        Setting values in dictionary returned should NOT change the value of the SimNode.
        """
        pass

    @abstractmethod
    def get_input_variables(self) -> dict:
        """
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

    def __init__(self):
        self.starting_arrow = None
        self.arrows = []
        self.arrow_to_arrows = defaultdict(list)

    def add_arrow(self, arrow:SimArrow) -> None:
        if None==self.starting_arrow:
            self.starting_arrow = arrow
        for a in self.arrows:
            if a.target == arrow.source:
                self.arrow_to_arrows[a].append(arrow)
            if arrow.target == a.source:
                self.arrow_to_arrows[arrow].append(a)
        self.arrows.append(arrow)
        
    def update(self) -> bool:
        arrow_stack = [self.starting_arrow,]
        nodes_to_prior_states = dict()
        success = True
        self.starting_arrow.source.update()
        while arrow_stack and success:
            arrow = arrow_stack.pop()
            source = arrow.source
            target = arrow.target
            nodes_to_prior_states[source] = source.get_state_variables()
            target_prior_state = nodes_to_prior_states.get(target)
            chain_done = not arrow.update()
            if target_prior_state:
                success = target_prior_state == target.get_state_variables()
            else:
                arrow_stack.extend(self.arrow_to_arrows[arrow])
            if chain_done:
                break
        if not success:
            ## restore all nodes to prior state
            for node, prior_state in nodes_to_prior_states:
                node.__dict__.update(prior_state)
        return success