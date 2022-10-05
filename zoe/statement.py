from enum import Enum, auto


class Statement:
    class Kind(Enum):
        READ = auto()
        READLN = auto()
        WRITE = auto()
        WRITELN = auto()
        ASSIGN = auto()
        EXPR = auto()
        EMPTY = auto()

    def __init__(self, kind, expr=None, expr2=None):
        self.kind = kind
        self.expr = expr
        self.expr2 = expr2

    def __eq__(self, other):
        return self.kind == other.kind and self.expr == other.expr and self.expr2 == other.expr2

    def __ne__(self, other):
        return not (self == other)

    def empty(self):
        return self.kind == Statement.Kind.EMPTY

    def do(self, context):
        if self.kind == Statement.Kind.READ:
            context.read(self.expr)

        if self.kind == Statement.Kind.READLN:
            context.readln(self.expr)

        if self.kind == Statement.Kind.WRITE:
            context.write(self.expr)

        if self.kind == Statement.Kind.WRITELN:
            context.writeln(self.expr)

        if self.kind == Statement.Kind.ASSIGN:
            context.assign(self.expr, self.expr2)

        if self.kind == Statement.Kind.EXPR:
            context.do(self.expr)
