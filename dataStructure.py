#!/usr/bin/python
# coding: utf8


class VariableRangeValue:

    id = ""
    bit_vector_size = 0
    value = None
    range = [-float("inf"), 0, float("inf")]

    def __init__(self, size, variable_name, default_range):
        self.bit_vector_size = size
        self.id = variable_name
        self.value = None
        self.range = default_range


class Interval:

    id = ""
    range = [None, None, None]

    def __init__(self, default_range):
        self.range = default_range
