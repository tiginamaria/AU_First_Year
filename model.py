import operator


class Scope:

    def __init__(self, parent=None):
        self.parent = parent
        self.dict = {}

    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        elif self.parent:
            return self.parent[key]
        else:
            return Number(None)

    def __setitem__(self, key, value):
        self.dict[key] = value


class Number:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def evaluate(self, scope):
        return self


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        return self


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.is_true = if_true
        self.is_false = if_false

    def __sequence__(self, node, scope):
        next_op = Number(None)
        if node:
            for op in node:
                next_op = op.evaluate(scope)
        return next_op

    def evaluate(self, scope):
        if self.condition.evaluate(scope).value == 0:
            return self.__sequence__(self.is_false, scope)
        else:
            return self.__sequence__(self.is_true, scope)


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        var = self.expr.evaluate(scope)
        print(var.value)
        return var


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        for i, arg in enumerate(function.args):
            call_scope[arg] = self.args[i].evaluate(scope)
        next_op = Number(None)
        for op in function.body:
            next_op = op.evaluate(call_scope)
        return next_op


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: None if (b == 0) else a // b,
        '%': lambda a, b: None if (b == 0) else a % b,
        '==': lambda a, b: int(a == b),
        '!=': lambda a, b: int(a != b),
        '<': lambda a, b: int(a < b),
        '>': lambda a, b: int(a > b),
        '<=': lambda a, b: int(a <= b),
        '>=': lambda a, b: int(a >= b),
        '&&': lambda a, b: int(a and b),
        '||': lambda a, b: int(a or b)
    }

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def evaluate(self, scope):
        a = self.lhs.evaluate(scope).value
        b = self.rhs.evaluate(scope).value
        return Number(self.ops[self.op](a, b))


class UnaryOperation:

    ops = {
        '-': lambda a: a if (a == 0) else -a,
        '!': lambda a: int(not a)
    }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        a = self.expr.evaluate(scope).value
        return Number(self.ops[self.op](a))


def example():

    parent = Scope()
    parent["foo"] = Function(
        ('hello', 'world'),
        [Print(BinaryOperation(Reference('hello'), '+', Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(
        FunctionDefinition('foo', parent['foo']),
        [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def my_tests():

    calculus = Scope()
    calculus['sum'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '+', Reference('b')))])
    calculus['div'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '/', Reference('b')))])
    calculus['dif'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '-', Reference('b')))])
    calculus['compare'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '<', Reference('b')))])
    calculus['dif_compare'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '>', Reference('b')))])

    teacher = Scope(calculus)
    read_x = Read('x')
    read_y = Read('y')
    print('Teacher x = ', end=' ')
    read_x.evaluate(teacher)
    print('Teacher y = ', end=' ')
    read_y.evaluate(teacher)
    print('Teacher x + y = ? ')
    print('Student x + y = ', end=' ')
    FunctionCall(FunctionDefinition('sum', calculus['sum']),
                 [teacher['x'], teacher['y']]).evaluate(teacher)
    print('Teacher x / y = ? ')
    print('Student x / y = ', end=' ')
    FunctionCall(FunctionDefinition('div', calculus['div']),
                 [teacher['x'], teacher['y']]).evaluate(teacher)
    print('Teacher x < y ? ')
    print('Student x < y ', end=' ')
    FunctionCall(FunctionDefinition('compare', calculus['compare']),
                 [teacher['x'], teacher['y']]).evaluate(teacher)
    read_z = Read('z')
    print('Teacher z = ', end=' ')
    read_z.evaluate(teacher)
    dif = BinaryOperation(teacher['x'], '-', teacher['y'])
    print('Teacher x - y > z ? ')
    print('Student x - y > z ', end=' ')
    FunctionCall(FunctionDefinition(
        'dif_compare', calculus['dif_compare']),
        [dif, teacher['z']]).evaluate(teacher)
    cond = BinaryOperation(teacher['x'], '>=', teacher['y'])
    print('Teacher if (x - y != z) then write(x) else write(z)  ? ')
    print('Student ..thinking.. ', end=' ')
    Print(Conditional(BinaryOperation(
        dif, '!=', teacher['z']),
        [teacher['x']], [teacher['z']])).evaluate(teacher)


if __name__ == '__main__':
    example()
    my_tests()
