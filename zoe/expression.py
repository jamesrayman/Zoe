from zoe.operator import Constant


class Expression:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        stack = []
        for op in self.expr:
            if op.arity == 0:
                stack.append(op())
            else:
                stack = stack[:-op.arity] + [op(*stack[-op.arity:])]

        return stack[0]

    def __eq__(self, other):
        return len(self.expr) == len(other.expr) \
        and all(
            type(a) == type(b) and
            a.arity == b.arity and
            (not isinstance(a, Constant) or a.constant.shallow_eq(b.constant))
            for a, b in zip(self.expr, other.expr)
        )


    def __ne__(self, other):
        return not (self.expr == other.expr)
