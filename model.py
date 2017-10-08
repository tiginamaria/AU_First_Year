class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.dictionary = {}

    def __getitem__(self, key):
        if key in self.dictionary:
            return self.dictionary[key]
        else:
            return self.parent[key]

    def __setitem__(self, key, value):
        self.dictionary[key] = value


class Number:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def evaluate(self, scope):
        return self


def evaluate_sequence(sequence, scope):
    result = None
    for operation in sequence or []:
        result = operation.evaluate(scope)
    return result


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

    def evaluate(self, scope):
        if self.condition.evaluate(scope) == Number(0):
            return evaluate_sequence(self.is_false, scope)
        else:
            return evaluate_sequence(self.is_true, scope)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        obj = self.expr.evaluate(scope)
        print(obj.value)
        return obj


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
        for arg, arg_value in zip(function.args, self.args):
            call_scope[arg] = arg_value.evaluate(scope)
        return evaluate_sequence(function.body, call_scope)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:
    OPS = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b,
        '%': lambda a, b: a % b,
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
        l_value = self.lhs.evaluate(scope).value
        r_value = self.rhs.evaluate(scope).value
        return Number(self.OPS[self.op](l_value, r_value))


class UnaryOperation:
    OPS = {
        '-': lambda a: -a,
        '!': lambda a: int(not a)
    }

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr_value = self.expr.evaluate(scope).value
        return Number(self.OPS[self.op](expr_value))


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
    calculus['subtr'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '-', Reference('b')))])
    calculus['compare'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '<', Reference('b')))])
    calculus['subtr_compare'] = Function(
        ('a', 'b'),
        [Print(BinaryOperation(Reference('a'), '>', Reference('b')))])

    teacher = Scope(calculus)
    read_x = Read('x')
    read_y = Read('y')
    print('Teacher: x = ', end=' ')
    read_x.evaluate(teacher)
    print('Teacher: y = ', end=' ')
    read_y.evaluate(teacher)
    print('Teacher: x + y = ? ')
    print('Student: x + y = ', end=' ')
    FunctionCall(
        FunctionDefinition('sum', calculus['sum']),
        [teacher['x'], teacher['y']]).evaluate(teacher)
    print('Teacher: x / y = ? ')
    print('Student: x / y = ', end=' ')
    FunctionCall(
        FunctionDefinition('div', calculus['div']),
        [teacher['x'], teacher['y']]).evaluate(teacher)
    print('Teacher: x < y ? ')
    print('Student: x < y ', end=' ')
    FunctionCall(
        FunctionDefinition('compare', calculus['compare']),
        [teacher['x'], teacher['y']]).evaluate(teacher)
    read_z = Read('z')
    print('Teacher: z = ', end=' ')
    read_z.evaluate(teacher)
    subtr = BinaryOperation(teacher['x'], '-', teacher['y'])
    print('Teacher: x - y > z ? ')
    print('Student: x - y > z ', end=' ')
    FunctionCall(FunctionDefinition(
        'subtr_compare', calculus['subtr_compare']),
        [subtr, teacher['z']]).evaluate(teacher)
    cond = BinaryOperation(teacher['x'], '>=', teacher['y'])
    cond1 = BinaryOperation(teacher['x'], '>=', teacher['y'])
    print('Teacher: if (x - y != z) then write(x) else write(z)  ? ')
    print('Student: ..thinking.. ', end=' ')
    Print(Conditional(BinaryOperation(
        subtr, '!=', teacher['z']),
        [teacher['x']], [teacher['z']])).evaluate(teacher)
    print('Teacher: My favorite number is 10?')
    a = Number(10)
    print('Student: ', end=' ')
    print(a == teacher['x'])
    print('Student: if (x < y) then (y) else (nothing) ?')
    print('Teacher: Such things are forbidden!!!')
    assert None is Conditional(
        BinaryOperation(teacher['x'], '<', subtr),
        [teacher['y']]).evaluate(teacher)


if __name__ == '__main__':
    example()
    my_tests()
