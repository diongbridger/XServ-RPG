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


class SimAtom(AbstractBaseClass):

    """
	SimAtom instances wrap sets of simulation state variables. They are the atomic components out of which complex simulations are assembled.
	The objects contained in the variable_* fields should NEVER change value unless the `update` method is called.
	"""

	## ToDo:
	##   - Write wrapper class that allows SimAtoms to negotiate a global update strategy using some number of feed-forward and feed-back operations.
	##   - SimAtom to act as a facade for a target instance, where the facade.update() method may be simpler/faster than target.update() but have the
	##   same input/output signature, so that target.update() will only be run if target.variables_internal is read out.

	variables_input: Set[Object] = set()
	variables_output: Set = set()
	variables_internal: Set = set()
	objects_component: Set[SimAtom] = set()

	# @abstractmethod
	# def attach(self, other) -> Optional[SimAtom]:
	# 	"""
	# 	Implementations should do exactly one of the following for any given value of `other`:
	# 	0. Return Optional.empty()
	# 	1. Return Optional.of(obj) where `obj` is a new SimAtom instance containing all of the variables belonging to both of the input objects.
	# 	"""
	# 	pass

	@abtractmethod
	def update(self):
		"""
		Update the internal and output variables of the object to reflect changes to the input variables.
		"""
		pass



## ToDo: think through how SimAtom instances can be instantiated & deleted at run time. Should there be a special class to mediate this?

## ToDo: Seperate examples folder
	

if __name__ == "__main__":
	main()
