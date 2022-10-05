from zoe.interpreter import run
from io import StringIO


def sim(program_text, input_text):
    istream = StringIO(input_text)
    ostream = StringIO()
    run(program_text, istream, ostream, ostream)

    return ostream.getvalue()


def sim_assert(program_text, input_text, expected=None):
    if expected is None:
        expected = input_text
        input_text = ''

    actual = sim(program_text, input_text)
    assert actual == expected


def sim_assert_file(path, input_text, expected=None):
    with open(path) as f:
        prg = f.read()
        sim_assert(prg, input_text, expected)


def lenient_eq(a, b):
    a = a.rstrip().splitlines()
    b = b.rstrip().splitlines()
    return len(a) == len(b) and all(al.rstrip() == bl.rstrip() for al, bl in zip(a, b))


def sim_assert_lenient(program_text, input_text, expected):
    actual = sim(program_text, input_text)

    assert lenient_eq(actual, expected)


def sim_assert_error(program_text, expected):
    actual = sim(program_text, '')
    assert actual.startswith('Error:\n')
    error = actual.splitlines()[1].strip()

    assert error == expected
