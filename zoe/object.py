from enum import Enum, auto
from zoe.exception import (
    NonSymbolicAssignmentException, IndexOutOfBoundsException, IllegalCastException,
    IllegalOperationException
)
from zoe.token import Token
from zoe.symbol import Symbol


def make_string(s):
    return Object(list(s), Object.Kind.STRING)


def make_int(x):
    return Object(int(x), Object.Kind.INT)


def make_list(v):
    return Object(v, Object.Kind.LIST)


def make_block(b):
    return Object(b, Object.Kind.BLOCK)


def make_symbol(symbol, symbol_table):
    return Object(symbol=symbol, symbol_table=symbol_table)


def make_object(token, symbol_table):
    if token.kind == Token.Kind.NUMBER:
        return make_int(token.value)

    if token.kind == Token.Kind.STRING:
        return make_string(token.value)

    if token.kind == Token.Kind.BLOCK:
        return make_block(token.value)

    if token.kind == Token.Kind.ID:
        return make_symbol(Symbol(token.value), symbol_table)

    return None


class Object:
    class Kind(Enum):
        INT = auto()
        STRING = auto()
        LIST = auto()
        BLOCK = auto()

    def __init__(self, value=None, kind=None, symbol=None, symbol_table=None):
        self._value = value
        self._kind = kind
        self._symbol = symbol
        self._symbol_table = symbol_table

    def value(self):
        if self.is_symbolic():
            return self._symbol_table.get(self._symbol).value()
        else:
            return self._value

    def set(self, other):
        if self.is_symbolic():
            self._symbol_table.set(self._symbol, other)
        else:
            raise NonSymbolicAssignmentException()

    def kind(self):
        if self.is_symbolic():
            return self._symbol_table.get(self._symbol).kind()
        else:
            return self._kind

    def is_symbolic(self):
        return self._symbol is not None

    def kind_str(self):
        if self.kind() == Object.Kind.INT:
            return 'Integer'

        if self.kind() == Object.Kind.STRING:
            return 'String'

        if self.kind() == Object.Kind.LIST:
            return 'List'

        if self.kind() == Object.Kind.BLOCK:
            return 'Block'

    def concrete(self):
        if self.is_symbolic():
            return Object(kind=self.kind(), value=self.value())

        if self.kind() == Object.Kind.LIST:
            return Object(
                kind=Object.Kind.LIST,
                value=[obj.concrete() for obj in self.value()]
            )

        return self

    def is_char(self):
        return self.kind() == Object.Kind.STRING and len(self.value()) == 1

    def shallow_eq(self, other):
        return self._symbol == other._symbol \
           and self._kind == other._kind \
           and self._value == other._value

    def __bool__(self):
        if self.kind() == Object.Kind.INT:
            return self.value() != 0
        else:
            return len(self.value()) != 0

    def __repr__(self):
        return f'({self.kind()}, {self.value()})'

    def __str__(self):
        if self.kind() == Object.Kind.INT:
            return str(self.value())

        if self.kind() == Object.Kind.STRING:
            return ''.join(self.value())

        if self.kind() == Object.Kind.LIST:
            return '[' + ', '.join(str(x) for x in self.value()) + ']'

        if self.kind() == Object.Kind.BLOCK:
            raise IllegalCastException('Block', 'String')

    def __int__(self):
        if self.kind() == Object.Kind.INT:
            return self.value()

        if self.kind() == Object.Kind.STRING:
            try:
                return int(''.join(self.value()))
            except ValueError:
                raise IllegalCastException('non-numeric String', 'Integer')

        if self.kind() == Object.Kind.LIST:
            raise IllegalCastException('List', 'Integer')

        if self.kind() == Object.Kind.BLOCK:
            raise IllegalCastException('Block', 'Integer')

    def __getitem__(self, index):
        if isinstance(index, int):
            index = make_int(index)

        if index.kind() != Object.Kind.INT:
            raise IllegalOperationException('@', self, index)

        if self.is_symbolic():
            return Object(symbol=self._symbol[index.value()], symbol_table=self._symbol_table)
        else:
            if self.kind() == Object.Kind.LIST or self.kind() == Object.Kind.STRING:
                if -len(self.value()) <= index.value() < len(self.value()):
                    res = self.value()[index.value()]
                    if self.kind() == Object.Kind.STRING:
                        res = make_string(res)
                    return res
                else:
                    raise IndexOutOfBoundsException(index.value())
            else:
                raise IllegalOperationException('@', self, index)

    def __len__(self):
        if self.kind() != Object.Kind.LIST and self.kind() != Object.Kind.STRING:
            raise IllegalOperationException('#', self)

        return len(self.value())

    def __eq__(self, other):
        return self.kind() == other.kind() and self.value() == other.value()

    def __ne__(self, other):
        return self.kind() != other.kind() or self.value() != other.value()

    def __lt__(self, other):
        if self.kind() != other.kind() or self.kind() == Object.Kind.BLOCK:
            raise IllegalOperationException('<', self, other)

        return self.value() < other.value()

    def __le__(self, other):
        if self.kind() != other.kind() or self.kind() == Object.Kind.BLOCK:
            raise IllegalOperationException('<=', self, other)

        return self.value() <= other.value()

    def __gt__(self, other):
        if self.kind() != other.kind() or self.kind() == Object.Kind.BLOCK:
            raise IllegalOperationException('>', self, other)

        return self.value() > other.value()

    def __ge__(self, other):
        if self.kind() != other.kind() or self.kind() == Object.Kind.BLOCK:
            raise IllegalOperationException('>=', self, other)

        return self.value() >= other.value()
