#!/usr/bin/python
# coding: utf8

import ast
import operator

operators = {
             ast.Add: operator.add,
             ast.Sub: operator.sub,
             ast.Mult: operator.mul,
             ast.Div: operator.truediv,
             ast.Pow: operator.pow,
             ast.BitXor: operator.xor,
             ast.USub: operator.neg
            }

logical_operators = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.lt,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge
}

comparison_sign = {
    ast.Eq: "==",
    ast.NotEq: "!=",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">="
}

opposite_comparison = {
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.Lt: ast.GtE,
    ast.LtE: ast.Gt,
    ast.Gt: ast.LtE,
    ast.GtE: ast.Lt
}
