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

    def accept(self, visitor):
        return visitor.visit_number(self)


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

    def accept(self, visitor):
        return visitor.visit_function(self)


class FunctionDefinition:
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


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

    def accept(self, visitor):
        return visitor.visit_conditional(self)


class Print:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        obj = self.expr.evaluate(scope)
        print(obj.value)
        return obj

    def accept(self, visitor):
        return visitor.visit_print(self)


class Read:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_read(self)


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

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class Reference:
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]

    def accept(self, visitor):
        return visitor.visit_reference(self)


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

    def accept(self, visitor):
        return visitor.visit_binary_operation(self)


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

    def accept(self, visitor):
        return visitor.visit_unary_operation(self)
