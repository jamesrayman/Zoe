from zoe.test import sim_assert, sim_assert_error


def test_newline_sequence():
    sim_assert('''
        writeln 'a'
        writeln 'b'
    ''', 'a\nb\n')


def test_semicolon_sequence():
    sim_assert("writeln 'a'; writeln 'b'", 'a\nb\n')


def test_extraneous():
    sim_assert('''

        writeln\t\t 'a'
        ;  ;;

        writeln 'b' \t;

    ''', 'a\nb\n')


def test_op_extend_back():
    sim_assert('write 5\n*5', '25')


def test_op_extend_forward():
    sim_assert('write 5+\n5', '10')


def test_unary_op_no_extend_back():
    sim_assert('write 5\n+5', '5')
    sim_assert('write 5\n-5', '5')


def test_semicolon_no_extend():
    sim_assert('write 5;+5', '5')
    sim_assert_error('write 5+;5', 'Invalid expression')


def test_op_extend_forward_back():
    sim_assert('write 8-\n-8', '16')


def test_error_after_write():
    sim_assert('writeln 7; 1 / 0', '7\nError:\nDivision by 0\n')
