from zoe.object import make_string, Object


class Context:
    def __init__(self, istream, ostream, program):
        self.istream = istream
        self.ostream = ostream
        self.todo = program.statements[::-1]
        self.prev_char = ''

    def write(self, expr):
        self.ostream.write(str(expr.evaluate()))

    def writeln(self, expr):
        self.ostream.write(str(expr.evaluate()) + '\n')

    def read(self, expr):
        if self.prev_char == '':
            self.prev_char = self.istream.read(1)
        while self.prev_char.isspace():
            self.prev_char = self.istream.read(1)

        s = ''

        while self.prev_char != '' and not self.prev_char.isspace():
            s += self.prev_char
            self.prev_char = self.istream.read(1)

        expr.evaluate().set(make_string(s))

    def readln(self, expr):
        if self.prev_char == '\n':
            s = self.prev_char
        else:
            s = self.prev_char + self.istream.readline()

        expr.evaluate().set(make_string(s))
        self.prev_char = ''

    def assign(self, lhs, rhs):
        lhs.evaluate().set(rhs.evaluate())

    def do(self, expr):
        res = expr.evaluate()
        if res.kind() == Object.Kind.BLOCK:
            self.todo += res.value().statements[::-1]

    def execute(self):
        while len(self.todo) > 0:
            statement = self.todo.pop()
            statement.do(self)
