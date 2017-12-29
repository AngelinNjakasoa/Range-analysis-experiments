#!/usr/bin/python
# coding: utf8

"""
 Contains range related data structures
 List of data structures:
     - VariableRangeValue
"""

class VariableRangeValue(object):

    """
     Contains the range [lower_bound, 0, upper_bound]
     Initialize the range to [-inf, 0, +inf]
    """

    identifier = ""
    bit_vector_size = 0
    value = None
    range = [-float("inf"), 0, float("inf")]
    LOWER_BOUND = 0
    UPPER_BOUND = 2

    def __init__(self, size, variable_name, default_range):
        self.bit_vector_size = size
        self.identifier = variable_name
        self.value = None
        self.range = default_range

    def set_lower_bound(self, new_bound):
        """
         Sets the lower bound value
        """
        self.range[VariableRangeValue.LOWER_BOUND] = new_bound

    def set_upper_bound(self, new_bound):
        """
         Sets the upper bound value
        """
        self.range[VariableRangeValue.UPPER_BOUND] = new_bound
