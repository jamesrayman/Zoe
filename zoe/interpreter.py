from zoe.tokenizer import tokenize
from zoe.parser import parse
from zoe.context import Context
import sys


def run(program_text, istream=sys.stdin, ostream=sys.stdout, estream=sys.stderr):
    try:
        tokens = tokenize(program_text)

        program = parse(tokens)
        context = Context(istream, ostream, program)

        context.execute()
        return 0
    except Exception as e:
        print('Error:', file=estream)
        print(e, file=estream)
        return 1
