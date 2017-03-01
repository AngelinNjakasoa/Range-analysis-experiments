#!/usr/bin/python

import ast
import astunparse
import visitorIteration
import sys

src = open(sys.argv[1]).read()
node = ast.parse(src)
visitor = visitorIteration.VisitorRangeAbstract()
visitor.visit(node)
