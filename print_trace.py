#!/usr/bin/python
# coding: utf8


"""
 print_trace contains all class related to tracing
"""
class PrintTrace(object):

    """
    Formats and print:
     - register variable id
     - assignement
     - content of while node
     - statement
     - content of else node
     - point:
         - id of the variable
         - variable's value
         - size of the Bitvector
         - range<lower_bound, 0, upper_bound>
    """

    def __init__(self):
        pass

    @staticmethod
    def print_register_variable_id(variable_id):
        """
         Prints a variable identifier
        """
        print "Variable id: " + str(variable_id)

    @staticmethod
    def print_assignment_update(id_node, element_id, evaluated_value):
        """
         Prints identifier and its mewly assigned value
        """
        print "P%s: Assignment id(%s) = %s" % (id_node, element_id, str(evaluated_value))

    @staticmethod
    def print_while_node(id_node, node):
        """
         Prints the statement of a while node and the while node number
        """
        print "P" + str(id_node) + ": While(" + str(node) + ")"

    @staticmethod
    def print_statement(id_node, statement_name, left_id, operator, comparator):
        """
         Prints a node number and the while node statement
        """
        string_print = "P" + str(id_node) + ": " + statement_name + "("
        string_print += str(left_id) + " " + operator + " " + str(comparator) + ")"
        print string_print

    @staticmethod
    def print_else_node(id_node, node):
        """
         Prints a else node number and its statement
         Its statement is the opposite of the If statement
        """
        print "P" + str(id_node) + ": Else(" + str(node) + ")"

    @staticmethod
    def print_state(state_number):
        """
         Prints a state number
        """
        print "State: P(%s)" % (str(state_number))

    @staticmethod
    def print_point(variable_id, value, lower_bound, median, upper_bound):
        """
         Prints informations about a point
         Bv: bitvector
         Bv.size: bitvector size
         Bv.id: variable identifier
         Bv.value: variable's value
         range: the range value <lower_bound, 0, upper_bound>
        """
        print "  Bv(size=64, id=%s, value=%s), VariableRangeValue(id=%s, range=<%s, %s, %s>)"\
            % (str(variable_id), str(value), variable_id,
               str(lower_bound), str(median), str(upper_bound))
