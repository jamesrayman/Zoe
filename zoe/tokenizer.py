from zoe.token import Token
from zoe.automaton import Automaton
from zoe.exception import (
    UnclosedStringLiteralException, UnknownTokenException
)
from enum import Enum, auto
import re


class State(Enum):
    CLEAR = auto()
    SYMBOL = auto()
    NUMBER = auto()
    STRING = auto()
    ID = auto()


def prefix(expr):
    return lambda s: re.fullmatch(expr + '.*', s, re.DOTALL)


def suffix(expr):
    return lambda s: re.fullmatch('.*' + expr, s, re.DOTALL)


def cut(i):
    return lambda s: s[i:]


def keep(i):
    return lambda s: s[-i:]


def identity(mem):
    return mem


def constant(k):
    return lambda mem: k


def symbol(text, kind, length=1):
    return (
        lambda s: s.startswith(text) and len(s) >= length,
        State.CLEAR,
        cut(len(text)),
        constant(Token(kind))
    )


token_transitions = {
    State.CLEAR: (
        (
            prefix('[0-9]'),
            State.NUMBER,
            identity,
            constant(None)
        ),
        (
            prefix("'"),
            State.STRING,
            cut(1),
            constant(None)
        ),
        (
            prefix('[A-Z_a-z]'),
            State.ID,
            identity,
            constant(None)
        ),
        (
            prefix('[\r\n]'),
            State.CLEAR,
            cut(1),
            constant(Token(Token.Kind.NEWLINE))
        ),
        (
            prefix('\\s'),
            State.CLEAR,
            cut(1),
            constant(None)
        ),
        (
            prefix('.'),
            State.SYMBOL,
            identity,
            constant(None)
        )
    ),
    State.STRING: (
        (
            suffix("'"),
            State.CLEAR,
            constant(''),
            lambda mem: Token(Token.Kind.STRING, mem[:-1])
        ),
    ),
    State.NUMBER: (
        (
            suffix('[^0-9]'),
            State.CLEAR,
            keep(1),
            lambda mem: Token(Token.Kind.NUMBER, int(mem[:-1]))
        ),
    ),
    State.ID: (
        (
            suffix('[^A-Z_a-z0-9]'),
            State.CLEAR,
            keep(1),
            lambda mem: Token(Token.Kind.ID, mem[:-1])
        ),
    ),
    State.SYMBOL: (
        symbol('**', Token.Kind.POW),
        symbol('/\\', Token.Kind.AND),
        symbol('\\/', Token.Kind.OR),
        symbol('/=', Token.Kind.NEQ),
        symbol('<=', Token.Kind.LEQ),
        symbol('>=', Token.Kind.GEQ),
        symbol(':=', Token.Kind.ASSIGN),

        symbol('(', Token.Kind.L_PAREN),
        symbol(')', Token.Kind.R_PAREN),
        symbol('[', Token.Kind.L_BRACK),
        symbol(']', Token.Kind.R_BRACK),
        symbol('{', Token.Kind.L_BRACE),
        symbol('}', Token.Kind.R_BRACE),
        symbol(';', Token.Kind.SEMICOLON),
        symbol('~', Token.Kind.NOT),
        symbol('#', Token.Kind.SIZE),
        symbol('@', Token.Kind.AT),
        symbol('*', Token.Kind.TIMES, 2),
        symbol('/', Token.Kind.DIVIDE, 2),
        symbol('%', Token.Kind.MOD),
        symbol('+', Token.Kind.PLUS),
        symbol('-', Token.Kind.MINUS),
        symbol('=', Token.Kind.EQ),
        symbol('<', Token.Kind.LESS, 2),
        symbol('>', Token.Kind.GREATER, 2),
        symbol(',', Token.Kind.COMMA),

        (
            suffix(r'[^/\\=:<>()\[\]{};~#@*%+,-]'),
            State.CLEAR,
            constant(''),
            lambda mem: Token(Token.Kind.UNKNOWN, mem.strip())
        )
    )
}


def tokenize(s):
    tokens = []

    s += '\n'
    a = Automaton(State.CLEAR, '', token_transitions)

    for c in s:
        tokens += a.process(c)

    if len(a.mem) > 0:
        if a.state == State.STRING:
            raise UnclosedStringLiteralException()
        else:
            tokens.append(Token(Token.Kind.UNKNOWN, a.mem.strip()))

    process_keywords(tokens)
    raise_unknown(tokens)

    return tokens


def process_keywords(tokens):
    keywords = {
        'read': Token(Token.Kind.READ),
        'readln': Token(Token.Kind.READLN),
        'write': Token(Token.Kind.WRITE),
        'writeln': Token(Token.Kind.WRITELN),
        'false': Token(Token.Kind.NUMBER, 0),
        'true': Token(Token.Kind.NUMBER, 1)
    }

    for i in range(len(tokens)):
        if tokens[i].kind == Token.Kind.ID:
            tokens[i] = keywords.get(tokens[i].value, tokens[i])

    return tokens


def raise_unknown(tokens):
    for token in tokens:
        if token.kind == Token.Kind.UNKNOWN:
            raise UnknownTokenException(token.value)
