import sys
import base64
from io import StringIO
from zoe.test import sim_assert_lenient

mess = '''WW91IGRpZCBpdCEgQ29uZ3JhdHVsYXRpb25zIQo='''


def pascal(n):
    ostream = StringIO()

    v = [1]

    for i in range(n):
        print(' '.join(map(str, v)), file=ostream)

        v = [0] + v + [0]
        u = []
        for j in range(i+2):
            u.append(v[j] + v[j+1])

        v = u

    return ostream.getvalue()


def entry():
    exit(main(sys.argv))


def main(argv):
    if len(argv) < 2:
        print('Please enter a file name. Example:', file=sys.stderr)
        print('    zoe! program.zoe', file=sys.stderr)
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

    for n in [1, 2, 3, 4, 5, 10, 24, 51, 104, 129, 199]:
        try:
            sim_assert_lenient(program, str(n), pascal(n))
        except AssertionError:
            print(f'Test case n = {n} failed.', file=sys.stderr)
            return 1

    print(base64.b64decode(mess).decode(), end='')

    return 0
