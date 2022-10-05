from zoe.test import sim_assert, sim_assert_error


def test_writeln():
    sim_assert("writeln 'Hello, world!'", 'Hello, world!\n')


def test_write():
    sim_assert("write 'Hello, world!'", 'Hello, world!')


def test_writeln_no_arg():
    sim_assert('writeln', '\n')


def test_write_no_arg():
    sim_assert_error('write', 'Empty expression')


echo_prg = 'read x; write x'


def test_read():
    sim_assert(echo_prg, 'hello', 'hello')


def test_read_word():
    sim_assert(echo_prg, 'hello\tx', 'hello')
    sim_assert(echo_prg, 'hello\na', 'hello')
    sim_assert(echo_prg, 'hello  a', 'hello')


def test_read_empty():
    sim_assert(echo_prg, '', '')
    sim_assert(echo_prg, '  ', '')


def test_read_non_symbol():
    sim_assert_error('read 1', 'Non-symbolic assignment')


def test_read_array_index():
    sim_assert(
        'x := [[2, 1, 0], [], 2]; read x @ 0 @ 1; write x',
        '10',
        '[[2, 10, 0], [], 2]'
    )


echo_echo_prg = 'read x; read y; write x; write y'


def test_read_word_word():
    sim_assert(echo_echo_prg, '', '')
    sim_assert(echo_echo_prg, 'hello world', 'helloworld')
    sim_assert(echo_echo_prg, '    a\n\t\t b c ', 'ab')


echoln_prg = 'readln x; write x'


def test_readln_line():
    sim_assert(echoln_prg, 'hello', 'hello')
    sim_assert(echoln_prg, 'hello\n', 'hello\n')
    sim_assert(echoln_prg, '  hello world  \n--', '  hello world  \n')


def test_readln_empty():
    sim_assert(echoln_prg, '', '')


skip_echoln_prg = 'read x; readln y; write y'


def test_read_word_line():
    sim_assert(skip_echoln_prg, 'hello   \tworld\nfoo', '   \tworld\n')
    sim_assert(skip_echoln_prg, 'hello\nworld', '\n')


def test_write_int():
    sim_assert('write 0', '0')
    sim_assert('write 001010', '1010')
    sim_assert('write 12345678901234567890', '12345678901234567890')
    sim_assert('write -12345678901234567890', '-12345678901234567890')


def test_write_list():
    sim_assert('write []', '[]')
    sim_assert("write [['a', 3], 5, 'hello']", '[[a, 3], 5, hello]')


def test_write_block():
    sim_assert_error('write { write 0 }', 'Illegal type conversion from Block to String')
