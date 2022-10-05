from enum import Enum, auto


class Token:
    class Kind(Enum):
        # Delimiters
        L_PAREN = auto()
        R_PAREN = auto()
        L_BRACK = auto()
        R_BRACK = auto()
        L_BRACE = auto()
        R_BRACE = auto()
        SEMICOLON = auto()
        NEWLINE = auto()

        # Operators
        NOT = auto()
        SIZE = auto()
        UMINUS = auto()
        UPLUS = auto()

        AT = auto()

        POW = auto()
        TIMES = auto()
        DIVIDE = auto()
        MOD = auto()
        PLUS = auto()
        MINUS = auto()

        AND = auto()
        OR = auto()

        EQ = auto()
        NEQ = auto()
        LESS = auto()
        GREATER = auto()
        LEQ = auto()
        GEQ = auto()

        # Constants
        STRING = auto()
        NUMBER = auto()

        # Other
        READ = auto()
        READLN = auto()
        WRITE = auto()
        WRITELN = auto()
        ID = auto()
        ASSIGN = auto()
        COMMA = auto()
        UNKNOWN = auto()

        # Processing information
        BLOCK = auto()
        VALUE = auto()

    def __init__(self, kind, value=None):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f'({self.kind}, {self.value})'

    def __eq__(self, other):
        return isinstance(other, Token) and self.kind == other.kind and self.value == other.value

    def is_left(self):
        return self.kind == Token.Kind.L_PAREN \
            or self.kind == Token.Kind.L_BRACK \
            or self.kind == Token.Kind.L_BRACE

    def is_binary_op(self):
        return self.kind == Token.Kind.AT \
            or self.kind == Token.Kind.POW \
            or self.kind == Token.Kind.TIMES \
            or self.kind == Token.Kind.DIVIDE \
            or self.kind == Token.Kind.MOD \
            or self.kind == Token.Kind.PLUS \
            or self.kind == Token.Kind.MINUS \
            or self.kind == Token.Kind.AND \
            or self.kind == Token.Kind.OR \
            or self.kind == Token.Kind.EQ \
            or self.kind == Token.Kind.NEQ \
            or self.kind == Token.Kind.LESS \
            or self.kind == Token.Kind.GREATER \
            or self.kind == Token.Kind.LEQ \
            or self.kind == Token.Kind.GEQ

    def is_unambiguous_binary_op(self):
        return self.kind == Token.Kind.AT \
            or self.kind == Token.Kind.POW \
            or self.kind == Token.Kind.TIMES \
            or self.kind == Token.Kind.DIVIDE \
            or self.kind == Token.Kind.MOD \
            or self.kind == Token.Kind.AND \
            or self.kind == Token.Kind.OR \
            or self.kind == Token.Kind.EQ \
            or self.kind == Token.Kind.NEQ \
            or self.kind == Token.Kind.LESS \
            or self.kind == Token.Kind.GREATER \
            or self.kind == Token.Kind.LEQ \
            or self.kind == Token.Kind.GEQ

    def is_unary_op(self):
        return self.kind == Token.Kind.NOT \
            or self.kind == Token.Kind.SIZE \
            or self.kind == Token.Kind.UMINUS \
            or self.kind == Token.Kind.UPLUS

    def is_op(self):
        return self.is_unary_op() or self.is_binary_op()

    def is_value(self):
        return self.kind == Token.Kind.VALUE
