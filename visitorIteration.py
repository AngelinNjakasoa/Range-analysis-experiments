#!/usr/bin/python
# coding: utf8

from rangeSemantic import *


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
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and n.id not in dict_id:
                self.semantic.register_variable_id(n.id)
                dict_id[n.id] = 1
        self.semantic.next_step_variables()
        self.generic_visit(node)
        print "#" * 80
        self.semantic.print_all_iteration()
        print "#" * 80

    def visit_BinOp(self, node):
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
        VisitorRangeAbstract.semantic.assignment_update(node)
        self.generic_visit(node)

    def visit_Compare(self, node):
        print "Compare node" + "State: " + str(VisitorRangeAbstract.id_node)
        self.generic_visit(node)

    def visit_While(self, node):
        self.semantic.extract_while_update(node)
        VisitorRangeAbstract.semantic.initialize_scope()
        for element in node.body:
            self.visit(element)
        VisitorRangeAbstract.semantic.finalize_scope()
        print "    DONE: While(" + str(node)
