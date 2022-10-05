from zoe.token import Token
from zoe.exception import (
    IllegalOperationException, DivideByZeroException, UnsupportedFeatureException
)
from zoe.object import Object, make_string, make_int, make_list, make_block


class Not:
    def __init__(self):
        self.arity = 1

    def __call__(self, x):
        return make_int(not bool(x))


class Size:
    def __init__(self):
        self.arity = 1

    def __call__(self, x):
        return make_int(len(x))


class UnaryPlus:
    def __init__(self):
        self.arity = 1

    def __call__(self, x):
        return make_int(int(x))


class UnaryMinus:
    def __init__(self):
        self.arity = 1

    def __call__(self, x):
        return make_int(-int(x))


class At:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return x[y]


class Pow:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        if x.kind() != Object.Kind.INT or y.kind() != Object.Kind.INT:
            raise IllegalOperationException('**', x, y)

        a = x.value()
        b = y.value()

        if b < 0 and a == 0:
            raise DivideByZeroException()

        if b < 0 and abs(a) != 1:
            raise UnsupportedFeatureException('Fractional values', True)

        return make_int(x.value() ** y.value())


class Times:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        if x.kind() != Object.Kind.INT and y.kind() != Object.Kind.INT:
            raise IllegalOperationException('*', x, y)

        if x.kind() != Object.Kind.INT:
            x, y = y, x

        if y.kind() == Object.Kind.INT:
            return make_int(x.value() * y.value())

        if y.kind() == Object.Kind.STRING:
            return make_string(x.value() * y.value())

        if y.kind() == Object.Kind.LIST:
            return make_list(x.value() * y.value())

        if y.kind() == Object.Kind.BLOCK:
            return make_block(y.value().repeat(x.value()))


class Divide:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        if x.kind() != Object.Kind.INT or y.kind() != Object.Kind.INT:
            raise IllegalOperationException('/', x, y)

        if y.value() == 0:
            raise DivideByZeroException()

        return make_int(x.value() // y.value())


class Mod:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        if x.kind() != Object.Kind.INT or y.kind() != Object.Kind.INT:
            raise IllegalOperationException('%', x, y)

        if y.value() == 0:
            raise DivideByZeroException()

        return make_int(x.value() % y.value())


class Plus:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        if x.kind() == y.kind() == Object.Kind.BLOCK:
            return make_block(x.value().extend(y.value()))

        if x.kind() == Object.Kind.BLOCK or y.kind() == Object.Kind.BLOCK:
            raise IllegalOperationException('+', x, y)

        if x.kind() == Object.Kind.STRING or y.kind() == Object.Kind.STRING:
            return make_string(str(x) + str(y))

        if x.kind() != y.kind():
            raise IllegalOperationException('+', x, y)

        if x.kind() == Object.Kind.INT:
            return make_int(x.value() + y.value())

        if x.kind() == Object.Kind.LIST:
            return make_list(x.value() + y.value())


class Minus:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        if x.kind() != Object.Kind.INT or y.kind() != Object.Kind.INT:
            raise IllegalOperationException('-', x, y)

        return make_int(x.value() - y.value())


class And:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return y if bool(x) else x


class Or:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return x if bool(x) else y


class Eq:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return make_int(x == y)


class Neq:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return make_int(x != y)


class Less:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return make_int(x < y)


class Greater:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return make_int(x > y)


class Leq:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return make_int(x <= y)


class Geq:
    def __init__(self):
        self.arity = 2

    def __call__(self, x, y):
        return make_int(x >= y)


class List:
    def __init__(self, size):
        self.arity = size

    def __call__(self, *args):
        return Object(list(args), kind=Object.Kind.LIST)


class Constant:
    def __init__(self, constant):
        self.arity = 0
        self.constant = constant

    def __call__(self):
        return self.constant


operators = {
    Token.Kind.AT: At,
    Token.Kind.SIZE: Size,
    Token.Kind.POW: Pow,
    Token.Kind.NOT: Not,
    Token.Kind.UPLUS: UnaryPlus,
    Token.Kind.UMINUS: UnaryMinus,
    Token.Kind.TIMES: Times,
    Token.Kind.DIVIDE: Divide,
    Token.Kind.MOD: Mod,
    Token.Kind.PLUS: Plus,
    Token.Kind.MINUS: Minus,
    Token.Kind.AND: And,
    Token.Kind.OR: Or,
    Token.Kind.EQ: Eq,
    Token.Kind.NEQ: Neq,
    Token.Kind.LESS: Less,
    Token.Kind.GREATER: Greater,
    Token.Kind.LEQ: Leq,
    Token.Kind.GEQ: Geq,
    Token.Kind.ID: Constant,
    Token.Kind.STRING: Constant,
    Token.Kind.NUMBER: Constant,
    Token.Kind.BLOCK: Constant
}
