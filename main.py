#!/usr/bin/python2.7
# coding: utf8

"""
 Test the Range Analysis on a python source code
"""
import sys
import ast
import visitor_iteration

def main():
    """
     Takes a python source code file as arguments and performs
     a range analysis
    """
    if len(sys.argv) == 2:
        source_file = open(sys.argv[1]).read()
        ast_node = ast.parse(source_file)
        visitor = visitor_iteration.VisitorRangeAbstract()
        try:
            visitor.visit(ast_node)
        except Exception:
            print "Invalid source code"
        else:
            sys.exit(1)

if __name__ == '__main__':
    main()
