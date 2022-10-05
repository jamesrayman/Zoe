import sys
from zoe.interpreter import run


def entry():
    exit(main(sys.argv))


def main(argv):
    if len(argv) < 2:
        print('Please enter a file name. Example:', file=sys.stderr)
        print('    zoe program.zoe', file=sys.stderr)
        return 1

    try:
        with open(argv[1], 'r') as f:
            program = f.read()
    except FileNotFoundError:
        print(f'File `{argv[1]}\' not found.', file=sys.stderr)
        return 1
    except OSError:
        print(f'File `{argv[1]}\' not readable.', file=sys.stderr)
        return 1

    return run(program)
