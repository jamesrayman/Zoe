from zoe.exception import UnsupportedFeatureException
from zoe.token import Token
from zoe.block import Block
from zoe.statement import Statement
from zoe.symboltable import SymbolTable
from zoe.object import make_string
from zoe.parseexpr import parse_expr
from zoe.operator import Constant
from zoe.expression import Expression
from zoe.bracketmatch import bracket_match


def parse_statement(tokens, symbol_table):
    if len(tokens) == 0:
        return Statement(Statement.Kind.EMPTY)

    if Token(Token.Kind.ASSIGN) in tokens:
        if tokens.count(Token(Token.Kind.ASSIGN)) > 1:
            raise UnsupportedFeatureException('Multiple assignment')

        i = tokens.index(Token(Token.Kind.ASSIGN))

        return Statement(
            Statement.Kind.ASSIGN,
            parse_expr(tokens[:i], symbol_table),
            parse_expr(tokens[i+1:], symbol_table)
        )

    if tokens[0].kind == Token.Kind.READ:
        return Statement(Statement.Kind.READ, parse_expr(tokens[1:], symbol_table))

    if tokens[0].kind == Token.Kind.READLN:
        return Statement(Statement.Kind.READLN, parse_expr(tokens[1:], symbol_table))

    if tokens[0].kind == Token.Kind.WRITE:
        return Statement(Statement.Kind.WRITE, parse_expr(tokens[1:], symbol_table))

    if tokens[0].kind == Token.Kind.WRITELN:
        if len(tokens) > 1:
            return Statement(Statement.Kind.WRITELN, parse_expr(tokens[1:], symbol_table))
        else:
            return Statement(Statement.Kind.WRITELN, Expression([Constant(make_string(''))]))

    return Statement(Statement.Kind.EXPR, parse_expr(tokens, symbol_table))


def extend_statements(tokens):
    new_tokens = []

    for token in tokens:
        if len(new_tokens) == 0:
            new_tokens.append(token)
            continue

        if token.kind == Token.Kind.NEWLINE and new_tokens[-1].is_binary_op():
            continue

        if token.is_unambiguous_binary_op() and new_tokens[-1].kind == Token.Kind.NEWLINE:
            new_tokens.pop()

        new_tokens.append(token)

    return new_tokens


def parse(tokens):
    bracket_match(tokens)
    tokens = extend_statements(tokens)

    block_stack = [Block([])]
    cur_statement = []

    symbol_table = SymbolTable()

    for token in tokens:
        if token.kind == Token.Kind.L_BRACE:
            block_stack.append(cur_statement)
            block_stack.append(Block([]))
            cur_statement = []
        elif token.kind == Token.Kind.R_BRACE:
            block_stack[-1].append(parse_statement(cur_statement, symbol_table))
            block = Token(Token.Kind.BLOCK, block_stack.pop())
            cur_statement = block_stack.pop() + [block]
        elif token.kind == Token.Kind.SEMICOLON or token.kind == Token.Kind.NEWLINE:
            block_stack[-1].append(parse_statement(cur_statement, symbol_table))
            cur_statement = []
        else:
            cur_statement.append(token)

    if len(cur_statement) > 0:
        block_stack[-1].append(parse_statement(cur_statement, symbol_table))

    return block_stack[0]
