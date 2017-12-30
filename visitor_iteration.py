#!/usr/bin/python2.7
# coding: utf8

"""
 Contains the VisitorRangeAbstract class.
"""

from range_semantic import ast
from range_semantic import ExtractRangeSemantic


class VisitorRangeAbstract(ast.NodeVisitor):

    """
    Visits the AST and track the range of values for each numeric variable
    """
    semantic = ExtractRangeSemantic()
    id_node = 0

    def __init__(self):
        self.dict_variable = dict()

    def visit_Module(self, node):
        """Extract numerical variables

        Walk through the module and get each numerical variable's id

        Arg:
            param1: module node
        Return:
            None
        """
        dict_id = dict()
        print "#" * 80
        for element in ast.walk(node):
            if isinstance(element, ast.Name) and element.id not in dict_id:
                self.semantic.register_variable_id(element.id)
                dict_id[element.id] = 1
        self.semantic.next_step_variables()
        self.generic_visit(node)
        print "#" * 80
        self.semantic.print_all_iteration()
        print "#" * 80

    def visit_BinOp(self, node):
        """
         Extracts a binary operation semantic and update the range
        """
        VisitorRangeAbstract.semantic.extract_binary_operation(node)
        self.generic_visit(node)

    def visit_If(self, node):
        """Range value analysis for If node

        Extracts statements and analyze the range value of if/else block
        Initialize and Finalize scope for if and else block in order to
        visit each nested block and apply the range values analysis to them.

        Arg:
            param1: if statement node
        Return:
            None
        """
        VisitorRangeAbstract.semantic.extract_if_statement_update(node)
        VisitorRangeAbstract.semantic.initialize_scope()
        for element in node.body:
            self.visit(element)
        VisitorRangeAbstract.semantic.finalize_scope()
        VisitorRangeAbstract.semantic.extract_else_statement_update(node)
        VisitorRangeAbstract.semantic.initialize_scope()
        for element in node.orelse:
            self.visit(element)
        VisitorRangeAbstract.semantic.finalize_scope()

    def visit_Assign(self, node):
        """
         Visits an assign node
         Update the range when an new value is assigned to a variable
        """
        VisitorRangeAbstract.semantic.assignment_update(node)
        self.generic_visit(node)

    def visit_Compare(self, node):
        """
         Visits a comparison node
         Update the range according to the comparison
        """
        print "Compare node" + "State: " + str(VisitorRangeAbstract.id_node)
        self.generic_visit(node)

    def visit_While(self, node):
        """
         Visits a While node
         Extract the semantic of the while node and create a scope for the
         while node's body, then visit the while node's body
        """
        self.semantic.extract_while_update(node)
        VisitorRangeAbstract.semantic.initialize_scope()
        for element in node.body:
            self.visit(element)
        VisitorRangeAbstract.semantic.finalize_scope()
        print "    DONE: While(" + str(node)
