#!/usr/bin/python2.7
# coding: utf8

"""
 Test the Range Analysis on a python source code
"""
import sys
import ast
import visitor_iteration

def main():
    if len(sys.argv) == 2:
        SOURCE_FILE = open(sys.argv[1]).read()
        AST_NODE = ast.parse(SOURCE_FILE)
        VISITOR = visitor_iteration.VisitorRangeAbstract()
        try:
            VISITOR.visit(AST_NODE)
        except:
            print "Invalid source code"
        else:
            sys.exit(1)

if __name__ == '__main__':
    main()
