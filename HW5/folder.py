from yat.model import *
from yat.printer import *
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
        v_true = []
        v_false = []
        for act in cond.is_true:
            v_true.append(act.accept(self))
        if cond.is_false:
            for act in cond.is_false:
                v_false.append(act.accept(self))
        return Conditional(cond.condition.accept(self), v_true, v_false)

    def visit_reference(self, reference):
        return reference

    def visit_print(self, print_expr):
        return Print(print_expr.expr.accept(self))

    def visit_read(self, read_expr):
        return read_expr

    def visit_binary_operation(self, bin_op):
        lhs = bin_op.lhs.accept(self)
        rhs = bin_op.rhs.accept(self)
        opr = bin_op.op
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

    def visit_unary_operation(self, un_op):
        ex = un_op.expr.accept(self)
        op = un_op.op
        if type(ex) == Number:
            return UnaryOperation(op, ex).evaluate(Scope())
        return UnaryOperation(op, ex)

    def visit_function_definition(self, func_def):
        v_body = []
        if func_def.function.body:
            for act in func_def.function.body:
                v_body.append(act.accept(self))
        return FunctionDefinition(
            func_def.name, Function(func_def.function.args, v_body))

    def visit_function_call(self, func_call):
        v_args = []
        if func_call.args:
            for arg in func_call.args:
                v_args.append(arg.accept(self))
        return FunctionCall(func_call.fun_expr.accept(self), v_args)


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
    a = BinaryOperation(name, '*', UnaryOperation('-', b))
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
    printer.visit(fluffy_penguin)
    f = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '+', Reference('b')))])
    printer.visit(FunctionCall(
        FunctionDefinition('fine', f), [Number(3), Number(10)]))

if __name__ == '__main__':
    tests()
