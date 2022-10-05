from zoe.exception import EmptyExpressionException, InvalidExpressionException
from zoe.expression import Expression
from zoe.object import make_object
from zoe.bracketmatch import bracket_match, match_index
from zoe.token import Token
import zoe.operator as op


def make_value(expr):
    return Token(Token.Kind.VALUE, Expression(expr))


def annotate_token(token, symbol_table):
    obj = make_object(token, symbol_table)

    if obj is None:
        return token
    else:
        return make_value([op.Constant(make_object(token, symbol_table))])


def parse_bracks(tokens):
    expr = []

    i = 0
    j = 0
    list_len = 1
    while i < len(tokens):
        if tokens[i].kind == Token.Kind.COMMA:
            expr += parse_value(tokens[j:i]).value.expr
            j = i + 1
            list_len += 1

        if tokens[i].is_left():
            i = match_index(tokens, i) + 1
        else:
            i += 1

    if j < i:
        expr += parse_value(tokens[j:i]).value.expr
    else:
        list_len -= 1

    expr.append(op.List(list_len))

    return make_value(expr)


def mark_unary_ops(tokens):
    new_tokens = []

    unary = True

    for token in tokens:
        if token.is_value():
            new_tokens.append(token)
            unary = False
        else:
            if unary and token.kind == Token.Kind.PLUS:
                new_tokens.append(Token(Token.Kind.UPLUS))
            elif unary and token.kind == Token.Kind.MINUS:
                new_tokens.append(Token(Token.Kind.UMINUS))
            else:
                new_tokens.append(token)

            unary = True

    return new_tokens


def check_bracket_free_expr(tokens):
    expect_value = True

    for token in tokens:
        if expect_value:
            if token.is_value():
                expect_value = False
            elif not token.is_unary_op():
                raise InvalidExpressionException()
        else:
            if not token.is_binary_op():
                raise InvalidExpressionException()
            expect_value = True

    if expect_value:
        raise InvalidExpressionException()


def simplify_binary_ops(tokens, operators):
    new_tokens = []

    i = 0
    while i < len(tokens):
        if tokens[i].kind in operators:
            j = i + 1
            while not tokens[j].is_value():
                j += 1
            next_i = j + 1

            new_tokens[-1].value.expr += tokens[j].value.expr

            j -= 1
            while j >= i:
                new_tokens[-1].value.expr.append(op.operators[tokens[j].kind]())
                j -= 1

            i = next_i
        else:
            new_tokens.append(tokens[i])
            i += 1

    return new_tokens


def simplify_unary_ops(tokens, operators):
    new_tokens = []

    for token in reversed(tokens):
        if token.kind in operators:
            j = 1
            while not new_tokens[-j].is_value():
                j += 1

            k = j
            j -= 1
            while j > 0:
                new_tokens[-k].value.expr.append(op.operators[new_tokens[-j].kind]())
                j -= 1

            if -k + 1 != 0:
                new_tokens = new_tokens[:-k+1]
            new_tokens[-1].value.expr.append(op.operators[token.kind]())
        else:
            new_tokens.append(token)

    return new_tokens[::-1]


def parse_bracket_free_value(tokens):
    tokens = mark_unary_ops(tokens)
    check_bracket_free_expr(tokens)

    tokens = simplify_binary_ops(tokens, [Token.Kind.AT])
    tokens = simplify_unary_ops(tokens, [Token.Kind.SIZE])
    tokens = simplify_binary_ops(tokens, [Token.Kind.POW])
    tokens = simplify_unary_ops(tokens, [Token.Kind.UPLUS, Token.Kind.UMINUS, Token.Kind.NOT])
    tokens = simplify_binary_ops(tokens, [Token.Kind.TIMES, Token.Kind.DIVIDE, Token.Kind.MOD])
    tokens = simplify_binary_ops(tokens, [Token.Kind.PLUS, Token.Kind.MINUS])
    tokens = simplify_binary_ops(tokens, [
        Token.Kind.LESS, Token.Kind.GREATER, Token.Kind.LEQ, Token.Kind.GEQ
    ])
    tokens = simplify_binary_ops(tokens, [Token.Kind.EQ, Token.Kind.NEQ])
    tokens = simplify_binary_ops(tokens, [Token.Kind.AND])
    tokens = simplify_binary_ops(tokens, [Token.Kind.OR])

    return tokens[0]


def parse_value(tokens):
    if len(tokens) == 0:
        raise EmptyExpressionException()

    bracket_free_tokens = []
    i = 0

    while i < len(tokens):
        if tokens[i].is_left():
            j = match_index(tokens, i)

            if tokens[i].kind == Token.Kind.L_PAREN:
                bracket_free_tokens.append(parse_value(tokens[i+1:j]))
            else:
                bracket_free_tokens.append(parse_bracks(tokens[i+1:j]))

            i = j + 1
        else:
            bracket_free_tokens.append(tokens[i])
            i += 1

    return parse_bracket_free_value(bracket_free_tokens)


def parse_expr(tokens, symbol_table):
    bracket_match(tokens)

    return parse_value(
        [annotate_token(token, symbol_table) for token in tokens]
    ).value
