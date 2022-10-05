from zoe.exception import UnmatchedBracketException
from zoe.token import Token


def bracket_match(tokens):
    stack = []

    for i, token in enumerate(tokens):
        if token.is_left():
            stack.append(token)

        if token.kind == Token.Kind.R_PAREN:
            if len(stack) == 0:
                raise UnmatchedBracketException(')')
            if stack[-1].kind == Token.Kind.L_BRACK:
                raise UnmatchedBracketException('[')
            if stack[-1].kind == Token.Kind.L_BRACE:
                raise UnmatchedBracketException('{')
            stack.pop()

        if token.kind == Token.Kind.R_BRACK:
            if len(stack) == 0:
                raise UnmatchedBracketException(']')
            if stack[-1].kind == Token.Kind.L_PAREN:
                raise UnmatchedBracketException('(')
            if stack[-1].kind == Token.Kind.L_BRACE:
                raise UnmatchedBracketException('{')
            stack.pop()

        if token.kind == Token.Kind.R_BRACE:
            if len(stack) == 0:
                raise UnmatchedBracketException('}')
            if stack[-1].kind == Token.Kind.L_PAREN:
                raise UnmatchedBracketException('(')
            if stack[-1].kind == Token.Kind.L_BRACK:
                raise UnmatchedBracketException('[')
            stack.pop()

    if len(stack) > 0:
        if stack[0].kind == Token.Kind.L_PAREN:
            raise UnmatchedBracketException('(')
        if stack[0].kind == Token.Kind.L_BRACK:
            raise UnmatchedBracketException('[')
        if stack[0].kind == Token.Kind.L_BRACE:
            raise UnmatchedBracketException('{')


def match_index(tokens, i):
    left = tokens[i].kind
    right = {
        Token.Kind.L_PAREN: Token.Kind.R_PAREN,
        Token.Kind.L_BRACK: Token.Kind.R_BRACK,
        Token.Kind.L_BRACE: Token.Kind.R_BRACE,
    }[left]

    depth = 1

    for j, token in enumerate(tokens[i+1:]):
        if token.kind == left:
            depth += 1
        if token.kind == right:
            depth -= 1

        if depth == 0:
            return j + i + 1
