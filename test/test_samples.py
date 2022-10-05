from zoe.test import sim_assert_file


def fib():
    f = [0, 1]

    while len(f) < 100:
        f.append(f[-1] + f[-2])

    return str(f)


def fizzbuzz():
    s = '\n'
    for i in range(1, 101):
        if i % 3 == 0:
            s += 'Fizz'
        if i % 5 == 0:
            s += 'Buzz'
        if s[-1] == '\n':
            s += str(i)
        s += '\n'
    return s[1:]


def palindrome(s):
    return s + ' is ' + ('' if s == s[::-1] else 'not ') + 'a palindrome.\n'


def pow_(n):
    return f'The first {n} powers of 2 are:\n' \
        + '\n'.join(str(2 ** i) for i in range(n)) \
        + ('\n' if n != 0 else '')


def test_hello():
    sim_assert_file('hello.zoe', 'Hello, world!\n')


def test_fib():
    sim_assert_file('fib.zoe', fib() + '\n')


def test_fizzbuzz():
    sim_assert_file('fizzbuzz.zoe', fizzbuzz())


def test_fizzbuzz2():
    sim_assert_file('fizzbuzz2.zoe', fizzbuzz())


def test_palindrome():
    tcs = [
        'aaaaa',
        '',
        'hello',
        'Aaaaa',
        'aba c aba'
    ]
    for tc in tcs:
        sim_assert_file('palindrome.zoe', str(tc) + '\n', palindrome(tc))


def test_pow():
    for n in [0, 5, 60]:
        sim_assert_file('pow.zoe', str(n), pow_(n))


def test_sort():
    tcs = [
        '7XU SDY Ome KQi d72 0VO DCl 0te KF0 zSJ'.split(),
        'a aaa aaaaaa a aa aaaaa aa'.split(),
        '9 8 7 6 5 4 3 2 1'.split(),
        '82 5 33 93 28 15 73 21 97 30 97 32 85 91 81 2 95 60 7 24'.split(),
        ['a'],
        []
    ]

    for tc in tcs:
        sim_assert_file('sort.zoe', ' '.join(tc) + ' end', ' '.join(sorted(tc)) + '\n')
