from zoe.exception import (
    UnassignedSymbolException, IndexOutOfBoundsException, IllegalCastException,
    IllegalAssignmentException
)
from zoe.object import Object


class SymbolTable:
    def __init__(self):
        self.table = {}

    def get(self, symbol):
        if symbol.name not in self.table:
            raise UnassignedSymbolException(symbol.name)

        value = self.table[symbol.name]

        for i in symbol.index:
            value = value[i]

        return value

    def set(self, symbol, value):
        if symbol.name == 'zoe':
            raise IllegalAssignmentException('Illegal assignment of special symbol `zoe\'')

        value = value.concrete()

        if len(symbol.index) == 0:
            self.table[symbol.name] = value
        else:
            if symbol.name not in self.table:
                raise UnassignedSymbolException(symbol.name)

            target = self.table[symbol.name]

            for i in range(len(symbol.index)-1):
                target = target[symbol.index[i]]

            if -len(target) <= symbol.index[-1] < len(target):
                if target.kind() == Object.Kind.LIST:
                    target._value[symbol.index[-1]] = value
                elif target.kind() == Object.Kind.STRING:
                    if not value.is_char():
                        raise IllegalCastException('non-character', 'character')
                    target._value[symbol.index[-1]] = value._value[0]
                else:
                    raise IllegalCastException(target.kind_str(), 'iterable')
            else:
                raise IndexOutOfBoundsException(symbol.index[-1])
