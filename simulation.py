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
#   [x] Move examples into a separate file.
#   [x] Think through how to model causal graphs with closed loops. E.g. gears arranged in a ring.
#   [ ] Implement layered SimGraphs & "graphs of graphs" to represent simulation at varying levels of abstraction.


class GraphUpdateException(Exception):
    """
    Represents an /unexpected/ failure during an update operation of a SimGraph.
    """
    pass



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
        Return a subset of self.__dict__ containing all variables considered to be 'input' variables.
        """
        pass

    def get_variables(self) -> dict:
        """
        Return all simulation variables held by this instance.
        """
        return {**self.get_input_variables(), **self.get_state_variables()}


class SimArrow(AbstractBaseClass):

    """
    Arrows represent unidirection causal relationships between nodes.
    All arrows must implement an 'effect' which copies values from the source to the target.
    """

    source: SimNode
    target: SimNode

    def update(self) -> bool:
        """
        Effect an update of the target node's state given the state of the input node.
        """
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
        """
        Extend the graph with a new causal arrow.
        """
        if None==self.starting_arrow:
            self.starting_arrow = arrow
        for a in self.arrows:
            if a.target == arrow.source:
                self.arrow_to_arrows[a].append(arrow)
            if arrow.target == a.source:
                self.arrow_to_arrows[arrow].append(a)
        self.arrows.append(arrow)

    def update(self) -> bool:
        """
        Compute the next state of the graph given its current state. If we return False then no state variables of any SimNode in the graph should
        change after we return. If we return True then all active causal arrows should have effected their changes before we exit.
        """
        arrow_stack = [self.starting_arrow,]
        nodes_to_prior_states = {self.starting_arrow.source: self.starting_arrow.source.get_variables()}
        self.starting_arrow.source.update()
        success = True ## Using a flag rather than an exception as failure to update state is not necessarily an error.
        while arrow_stack:
            ## select target node to update
            arrow = arrow_stack.pop()
            source = arrow.source
            target = arrow.target
            target_prior_state = nodes_to_prior_states.get(target)
            if not target_prior_state:
                nodes_to_prior_states[target] = target.get_variables()
            ## Perform update 
            chain_done = not arrow.update()
            if target_prior_state:
                success &= (target_prior_state == target.get_variables())
                chain_done = True
            else:
                arrow_stack.extend(self.arrow_to_arrows[arrow])
            ## Undo all state changes if an inconsistency obtains
            if not success:
                ## Undo all state updates
                for node, prior_state in nodes_to_prior_states.items():
                    node.__dict__.update(prior_state)
            ## Check for premature exit
            if chain_done:
                break
        return success
