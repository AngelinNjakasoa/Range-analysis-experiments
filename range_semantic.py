#!/usr/bin/python
# coding: utf8

import ast
from print_trace import PrintTrace
from range_operator import operators
from range_operator import comparison_sign
from range_operator import opposite_comparison
from data_structure import VariableRangeValue
from lexical_scope_symbol_table import LexicalScopeSymbolTable


class ExtractRangeSemantic(PrintTrace):

    all_variable_id = list()
    vector_point = list()
    scope_symbol_table = LexicalScopeSymbolTable()
    id_node = 1

    def __init__(self):
        PrintTrace.__init__(self)
        self.id_node = 1

    def get_id_node(self):
        return self.id_node

    def register_variable_id(self, variable_id):
        self.all_variable_id.append(str(variable_id))
        self.print_register_variable_id(variable_id)

    def next_step_variables(self):
        self.vector_point.append(dict())
        if len(self.vector_point) > 1:
            for k, value in self.vector_point[-2].iteritems():
                if value != 0:
                    self.vector_point[-1][k] = VariableRangeValue(64, k, [None, None, None])
                    self.propagate_range(len(self.vector_point) - 1, k)
                    self.vector_point[-1][k].value = None
                    self.vector_point[-1][k].id = k
        else:
            for element in self.all_variable_id:
                self.vector_point[-1][element] = VariableRangeValue(64,
                                                                    element,
                                                                    [-float("inf"),
                                                                     0,
                                                                     float("inf")])
                self.vector_point[-1][element].id = element
        self.id_node = len(self.vector_point)

    def get_binary_operator_operands(self, node_left, node_right):
        left_op = node_left
        right_op = node_right
        if isinstance(node_left, ast.Name):
            left_op = self.scope_symbol_table.lookup_symbol(node_left.id)
        else:
            left_op = node_left
        if isinstance(node_right, ast.Name):
            right_op = self.scope_symbol_table.lookup_symbol(node_right.id)
        else:
            right_op = node_right
        return [left_op, right_op]

    def get_unary_operator_operand(self, operand):
        if isinstance(operand, ast.Name):
            return self.scope_symbol_table.lookup_symbol(operand.id)
        else:
            print "Error: bad operand"
            raise

    def eval_(self, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            operands = self.get_binary_operator_operands(node.left, node.right)
            print "Eval: operands - " + str(operands)
            return int(operators[type(node.op)](self.eval_(operands[0]), self.eval_(operands[1])))
        elif isinstance(node, ast.UnaryOp):
            operand = self.get_unary_operator_operand(node.operand)
            return int(operators[type(node.op)](self.eval_(operand)))
        print "Error: incorrect type in eval_"
        raise

    def propagate_range(self, point, var_id):
        prev_point = point - 1
        self.vector_point[point][var_id].range[0] = self.vector_point[prev_point][var_id].range[0]
        self.vector_point[point][var_id].range[1] = self.vector_point[prev_point][var_id].range[1]
        self.vector_point[point][var_id].range[2] = self.vector_point[prev_point][var_id].range[2]

    def reset_range(self, point, variable_id):
        for index in range(0, len(self.vector_point[point][variable_id].range)):
            self.vector_point[point][variable_id].range[index] = None
            index += 1

    def update_range_semantic(self, point, variable_id, value):
        index = 1
        self.reset_range(point, variable_id)
        if value == 0:
            self.vector_point[point][variable_id].range[index] = 0
            return 0
        index = (2 if value > 0 else 0)

        self.vector_point[point][variable_id].range[index] = (float('inf') \
                                                              if value > 0 else -float('inf'))

    def assignment_update(self, new_value):
        for element in new_value.targets:
            evaluated_value = self.eval_(new_value.value)
            node_value = ast.Num(evaluated_value)
            self.update_range_semantic(len(self.vector_point) - 1, element.id, evaluated_value)
            self.vector_point[-1][element.id].value = evaluated_value
            index_level = self.scope_symbol_table.get_current_level() - 1
            self.scope_symbol_table.bind_symbol(element.id,
                                                node_value,
                                                index_level,
                                                self.scope_symbol_table.get_last_offset(index_level))
            self.print_assignment_update(self.id_node, element.id, evaluated_value)
        self.next_step_variables()

    @staticmethod
    def get_statement(node, flag_opposite):
        collection = [None, None, None]
        comparator = node.test.comparators
        collection[0] = (comparison_sign[opposite_comparison[type(node.test.ops[0])]] \
                         if flag_opposite == 1 else comparison_sign[type(node.test.ops[0])])
        if isinstance(node.test.left, ast.Num):
            collection[1] = node.test.left.n
        elif isinstance(node.test.left, ast.Name):
            collection[1] = node.test.left.id
        if isinstance(comparator[0], ast.Num):
            collection[2] = comparator[0].n
        elif isinstance(comparator[0], ast.Name):
            collection[2] = comparator[0].id
        return collection

    def extract_while_update(self, node):
        operation = self.get_statement(node, 0)
        self.print_statement(self.id_node, "While", operation[1], operation[0], operation[2])
        self.next_step_variables()

    def extract_if_statement_update(self, node):
        operation = self.get_statement(node, 0)
        self.print_statement(self.id_node, "If", operation[1], operation[0], operation[2])
        self.next_step_variables()

    def extract_else_statement_update(self, node):
        operation = self.get_statement(node, 1)
        self.print_statement(self.id_node, "Else", operation[1], operation[0], operation[2])
        self.next_step_variables()

    def extract_binary_operation(self, node):
        pass

    def initialize_scope(self):
        self.scope_symbol_table.initialize_scope()

    def finalize_scope(self):
        self.scope_symbol_table.finalize_scope()

    def print_debug_level(self):
        for i in range(0, self.scope_symbol_table.get_size_level()):
            self.scope_symbol_table.dump_level(i)
        print "#" * 30 + "End of DEBUG LEVEL" + "#" * 30

    def print_all_iteration(self):
        point = 0
        self.print_debug_level()
        for element in self.vector_point:
            self.print_state(point + 1)
            for k in element:
                point_index = point
                lower_bound = self.vector_point[point_index][k].range[0]
                median = self.vector_point[point_index][k].range[1]
                upper_bound = self.vector_point[point_index][k].range[2]
                value = self.vector_point[point_index][k].value
                variable_id = self.vector_point[point_index][k].id
                self.print_point(variable_id, value, lower_bound, median, upper_bound)
            point += 1
