#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest


from simulation import SimNode, SimArrow, SimGraph


## this could be factored out into a non-test utilities class - will leave that for when it becomes necessary.
class BooleanNode(SimNode):
    """
    Simple switch with on/off state only.
    """
    def __init__(self):
        self.input_state = False

    def update(self):
        """
        Switches are in a sense simply just inputs. They have no internal mechanism, so there's nothing to do here.
        """
        return True

    def get_state_variables(self) -> dict:
        return dict()

    def get_input_variables(self) -> dict:
        return {"input_state": self.input_state}


class BooleanArrow(SimArrow):


    def __init__(self, source:BooleanNode, target:BooleanNode):
        self.source = source
        self.target = target

    def effect(self) -> bool:
        """
        Simply copy the input state to the output node.
        """
        self.target.input_state = self.source.input_state
        return True


@pytest.fixture
def boolean_node_1():
    return BooleanNode()

@pytest.fixture
def boolean_node_2():
    return BooleanNode()

@pytest.fixture
def boolean_arrow_1(boolean_node_1, boolean_node_2):
    return BooleanArrow(boolean_node_1, boolean_node_2)


def test_change_propagation(boolean_arrow_1, boolean_node_1, boolean_node_2):
    """
    Check that arrows actually propagate input changes effectually.
    """
    assert False == boolean_node_1.input_state
    assert False == boolean_node_2.input_state
    boolean_node_1.input_state = True
    assert boolean_arrow_1.update() ## propagate change
    assert True == boolean_node_1.input_state
    assert True == boolean_node_2.input_state
