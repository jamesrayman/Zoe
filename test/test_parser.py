from zoe.test import sim_assert, sim_assert_error


# Bracket matching
def test_paren_match():
    sim_assert('write ((0) + (0 + 0)) + (((0)))', '0')
    sim_assert_error('write ((0)) + (0 + 0)) + (((0)))', "Unmatched `)'")
    sim_assert_error('write ((0) + (0 + 0) + (((0)))', "Unmatched `('")


def test_brack_match():
    sim_assert_error('[', "Unmatched `['")
    sim_assert_error(']', "Unmatched `]'")


def test_brace_match():
    sim_assert_error('{', "Unmatched `{'")
    sim_assert_error('}', "Unmatched `}'")


def test_match_expr():
    sim_assert_error('[a := 0]', "Unmatched `['")
    sim_assert_error('(a := 0)', "Unmatched `('")


def test_bracket_mismatch():
    sim_assert_error('write [(0])', "Unmatched `('")
    sim_assert_error('write {(0})', "Unmatched `('")
    sim_assert_error('{ write [0}]', "Unmatched `['")
    sim_assert_error('write ([0)]', "Unmatched `['")
    sim_assert_error('write ({0)}', "Unmatched `{'")
    sim_assert_error('write [{0]}', "Unmatched `{'")


# Bracket parsing
def test_list_parsing():
    sim_assert('write []', '[]')
    sim_assert(
        'write [1 + 2 ** 4, ([0] + [1]) * (3 * 2 + 3), 0]',
        '[17, [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1], 0]'
    )
    sim_assert_error('write [,]', 'Empty expression')
    sim_assert_error('write [, 1]', 'Empty expression')
    sim_assert_error('write [0,, 1]', 'Empty expression')
    sim_assert('write [0,]', '[0]')
    sim_assert('write [1, 2, 3,]', '[1, 2, 3]')


# Bracket-free parsing
def test_invalid_expr():
    sim_assert_error('write @', 'Invalid expression')
    sim_assert_error('write @ 2', 'Invalid expression')
    sim_assert_error('write [1] @', 'Invalid expression')
    sim_assert_error('write 2 * * 2', 'Invalid expression')
    sim_assert_error('write 2 2', 'Invalid expression')
    sim_assert_error('write 2 #', 'Invalid expression')
    sim_assert_error('write 2 + #', 'Invalid expression')
    sim_assert_error('write #', 'Invalid expression')
    sim_assert_error('write write', 'Invalid expression')
    sim_assert_error('write (1, 1)', 'Invalid expression')


def test_valid_expr():
    sim_assert('write 2 *+-+ 2', '-4')


# Operator precedence
def test_strict_precedence():
    sim_assert('write 1 + 2 * 3', '7')
    sim_assert('write 2 * 3 + 1', '7')

    sim_assert('write #[[0], [1, 2], []] @ 1', '2')
    sim_assert('write #[0, 1] ** 3', '8')
    sim_assert('write -2 ** 4', '-16')
    sim_assert('write 2 > 3 + 2', '0')
    sim_assert('write 3 < 2 = 0', '1')
    sim_assert(r'write ~1 /\ 1 \/ 1', '1')
    sim_assert(r'write ~1 /\ (1 \/ 1)', '0')


def test_paren_precedence():
    sim_assert('write (1 + 2) * 3', '9')


def test_unary_chain_precedence():
    sim_assert_error(
        "write #+'5'",
        "Illegal operation `#' with operand of kind Integer"
    )


def test_ltr_precedence():
    sim_assert('write 14 / 5 * 5', '10')
    sim_assert('write 10002 / 100 / 3', '33')
    sim_assert('write 10 - 2 + 4 - 2 - 1', '9')


def test_right_unary_precedence():
    sim_assert('a := -4; write -2 ** -a', '-16')


# Constants
def test_true_false():
    sim_assert('write true', '1')
    sim_assert('write false', '0')
