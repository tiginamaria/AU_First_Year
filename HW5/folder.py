from model import *
from printer import *
import sys


class ConstantFolder:
    def visit(self, tree):
        return tree.accept(self)

    def visit_number(self, number):
        return number

    def block_expr(self, exprs):
        if exprs:
            return [expr.accept(self) for expr in exprs]

    def visit_conditional(self, cond):
        return Conditional(cond.condition.accept(self),
                           self.block_expr(cond.is_true),
                           self.block_expr(cond.is_false))

    def visit_reference(self, reference):
        return reference

    def visit_print(self, print_expr):
        return Print(print_expr.expr.accept(self))

    def visit_read(self, read_expr):
        return read_expr

    def visit_binary_operation(self, binary_operation):
        lhs = binary_operation.lhs.accept(self)
        rhs = binary_operation.rhs.accept(self)
        opr = binary_operation.op
        l_num = type(lhs) == Number
        r_num = type(rhs) == Number
        l_ref = type(lhs) == Reference
        r_ref = type(rhs) == Reference
        if opr == '*' and l_num and r_ref and lhs.value == 0:
            return Number(0)
        if opr == '*' and r_num and l_ref and rhs.value == 0:
            return Number(0)
        if opr == '-' and r_ref and l_ref and lhs.name == rhs.name:
            return Number(0)
        if l_num and r_num:
            return BinaryOperation(lhs, opr, rhs).evaluate(Scope())
        return BinaryOperation(lhs, opr, rhs)

    def visit_unary_operation(self, unary_operation):
        ex = unary_operation.expr.accept(self)
        op = unary_operation.op
        return UnaryOperation(unary_operation.op, ex).evaluate(Scope())

    def visit_function_call(self, function_call):
        fun_expr = function_call.fun_expr.accept(self)
        args = [expr.accept(self) for expr in function_call.args]
        return FunctionCall(fun_expr, args)

    def visit_function_definition(self, function_definition):
        args = function_definition.function.args
        for i in range(len(function_definition.function.body)):
            function_definition.function.body[i] = self.visit(
                function_definition.function.body[i])
        return function_definition


def tests():
    scope = Scope()
    folder = ConstantFolder()
    printer = PrettyPrinter()
    name = Number(3)
    b = BinaryOperation(Number(0), '*', Number(5))
    printer.visit(b)
    printer.visit(folder.visit(b))
    a = BinaryOperation(name, '*', Number(5))
    printer.visit(a)
    printer.visit(folder.visit(a))
    a = BinaryOperation(name, '*', Number(0))
    printer.visit(a)
    printer.visit(folder.visit(a))
    a = BinaryOperation(name, '*', b)
    printer.visit(a)
    printer.visit(folder.visit(a))
    a = UnaryOperation('-', Number(5))
    printer.visit(a)
    printer.visit(folder.visit(a))
    c = Conditional(BinaryOperation(
        Number(666), '>', BinaryOperation(
            Number(33), '+', Number(99))), [Number(3)], [Number(5)])
    printer.visit(c)
    printer.visit(folder.visit(c))
    a = Number(1)
    b = UnaryOperation('!', Number(3))
    fluffy_penguin = FunctionDefinition(
        'To_bE_Or_nOT_tO_Be', Function(
            ('a', 'b'), [Conditional(BinaryOperation(
                Number(666), '>', BinaryOperation(
                    Number(333), '+', Number(999))),
                    [Number(3)], [UnaryOperation('-', Number(999))])]))
    printer.visit(fluffy_penguin)
    printer.visit(folder.visit(fluffy_penguin))

if __name__ == '__main__':
    tests()
