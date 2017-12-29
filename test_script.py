#!/usr/bin/python2.7
# coding: utf8

"""
 Test the Range Analysis on a python source code
"""

import sys
import ast
import visitor_iteration

SOURCE_FILE = open(sys.argv[1]).read()
AST_NODE = ast.parse(SOURCE_FILE)
VISITOR = visitor_iteration.VisitorRangeAbstract()
VISITOR.visit(AST_NODE)
