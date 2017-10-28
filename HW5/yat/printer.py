from yat.model import *
import sys


class PrettyPrinter:
    def __init__(self):
        self.tabs = 0

    def visit(self, tree):
        tree.accept(self)
        print(';')

    def visit_number(self, number):
        print(number.value, end='')

    def visit_reference(self, reference):
        print(reference.name, end='')

    def visit_read(self, read_expr):
        print('read ' + read_expr.name, end='')

    def visit_print(self, print_expr):
        print('print ', end='')
        print_expr.expr.accept(self)

    def block_exprs(self, exprs):
        if exprs:
            self.tabs += 4
            for expr in exprs:
                print(self.tabs * ' ', end='')
                expr.accept(self)
                print(';')
            self.tabs -= 4

    def visit_conditional(self, cond):
        print('if (', end='')
        cond.condition.accept(self)
        print(') {')
        self.block_exprs(cond.is_true)
        print(self.tabs * ' ' + '}', end='')
        if cond.is_false:
            print(' else {')
            self.block_exprs(cond.is_false)
            print(self.tabs * ' ' + '}', end='')

    def visit_function_definition(self, func_def):
        print(
            'def ' + func_def.name + '(' + ', '.join(
                func_def.function.args) + ') {')
        self.block_exprs(func_def.function.body)
        print(self.tabs * ' ' + '}', end='')

    def visit_function_call(self, func_call):
        func_call.fun_expr.accept(self)
        print('(', end='')
        if func_call.args:
            next_arg = 0
            for arg in func_call.args:
                if next_arg:
                    print(', ', end='')
                next_arg = 1
                arg.accept(self)
        print(')', end='')

    def visit_binary_operation(self, bin_op):
        print('(', end='')
        bin_op.lhs.accept(self)
        print(')', end=' ')
        print(bin_op.op, end=' ')
        print('(', end='')
        bin_op.rhs.accept(self)
        print(')', end='')

    def visit_unary_operation(self, un_op):
        print(un_op.op, end='')
        print('(', end='')
        un_op.expr.accept(self)
        print(')', end='')


def my_small_test():
    scope = Scope()
    printer = PrettyPrinter()
    a = Number(1)
    b = UnaryOperation('!', Number(3))
    fluffy_penguin = FunctionDefinition(
        'To_bE_Or_nOT_tO_Be', Function(
            ('a', 'b'), [Conditional(BinaryOperation(
                Number(666), '>', BinaryOperation(
                    Number(333), '+', Number(999))),
                    [Number(3)],
                    [UnaryOperation('-', b)])]))

    printer.visit(fluffy_penguin)
    printer.visit(FunctionCall(
        Reference('fine'), [Number(3), Number(10)]))


if __name__ == '__main__':
    my_small_test()
