from zoe.test import lenient_eq
from zoe.challenge import pascal


def test_lenient_eq_trailing_empty_lines():
    assert lenient_eq('a\nb\n\n\n', 'a\nb\n   ')


def test_lenient_eq_trailing_whitespace():
    assert lenient_eq('a  \t\nb ', 'a\nb\t  ')


def test_lenient_eq_leading_whitespace():
    assert not lenient_eq('a\n b', 'a\nb')


def test_lenient_eq_middle_whitespace():
    assert not lenient_eq('x y\nb', 'x  y\nb')


def test_lenient_eq_middle_newline():
    assert not lenient_eq('a\nb', 'a\n\nb')


def test_lenient_eq_leading_newline():
    assert not lenient_eq('a\nb', '\na\nb')


def test_lenient_eq_extra_lines():
    assert not lenient_eq('a\n', 'a\nb')


def test_challenge():
    assert lenient_eq(pascal(1), '1')
    assert lenient_eq(pascal(5), '''\
1
1 1
1 2 1
1 3 3 1
1 4 6 4 1
    ''')

    assert lenient_eq(pascal(10), '''\
1
1 1
1 2 1
1 3 3 1
1 4 6 4 1
1 5 10 10 5 1
1 6 15 20 15 6 1
1 7 21 35 35 21 7 1
1 8 28 56 70 56 28 8 1
1 9 36 84 126 126 84 36 9 1
    ''')
