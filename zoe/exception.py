class UnclosedStringLiteralException(Exception):
    def __init__(self):
        super().__init__('Unclosed string literal')


class UnknownTokenException(Exception):
    def __init__(self, symbol):
        super().__init__(f'Unknown token `{symbol}\'')


class UnmatchedBracketException(Exception):
    def __init__(self, bracket):
        super().__init__(f'Unmatched `{bracket}\'')


class IllegalOperationException(Exception):
    def __init__(self, operator, x, y=None):
        if y is not None:
            kinds = x.kind_str() + ' and ' + y.kind_str()
            s = 's'
        else:
            kinds = x.kind_str()
            s = ''

        super().__init__(
            f'Illegal operation `{operator}\' with operand{s} of kind {kinds}'
        )


class DivideByZeroException(Exception):
    def __init__(self):
        super().__init__('Division by 0')


class NonSymbolicAssignmentException(Exception):
    def __init__(self):
        super().__init__('Non-symbolic assignment')


class EmptyExpressionException(Exception):
    def __init__(self):
        super().__init__('Empty expression')


class InvalidExpressionException(Exception):
    def __init__(self):
        super().__init__('Invalid expression')


class UnassignedSymbolException(Exception):
    def __init__(self, symbol):
        super().__init__(f'Unassigned symbol `{symbol}\' used in expression')


class IndexOutOfBoundsException(Exception):
    def __init__(self, index):
        super().__init__(f'Index {index} is out of bounds')


class IllegalCastException(Exception):
    def __init__(self, from_type, to_type):
        super().__init__(f'Illegal type conversion from {from_type} to {to_type}')


class IllegalAssignmentException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UnsupportedFeatureException(Exception):
    def __init__(self, feature, plural=False):
        is_ = 'is' if not plural else 'are'
        super().__init__(f'{feature} {is_} not supported')
