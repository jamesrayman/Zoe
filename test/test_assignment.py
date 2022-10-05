from zoe.test import sim_assert, sim_assert_error


def test_assign():
    sim_assert('foo := 10; write foo', '10')


def test_serial_assign():
    sim_assert('foo := 10; bar := foo; foo := 15; write bar', '10')


def test_serial_list_assign():
    sim_assert('foo := 10; bar := [foo]; foo := 15; write bar', '[10]')


def test_serial_nested_list_assign():
    sim_assert(
        'foo := 10; bar := [foo, [foo], [[foo]]]; foo := 15; write bar',
        '[10, [10], [[10]]]'
    )


def test_serial_string_assign():
    sim_assert("foo := 'a'; bar := 'b' + foo; foo := 'b'; write bar", 'ba')


def test_list_assignment():
    sim_assert('foo := [0, 1, 2]; foo @ 1 := 5; write foo', '[0, 5, 2]')


def test_string_assignment():
    sim_assert("foo := 'cat'; foo @ 2 := 'b'; write foo", 'cab')


def test_nested_list_assignment():
    sim_assert('foo := [0, [0, 1, 2], 2]; foo @ 1 @ 0 := [2]; write foo', '[0, [[2], 1, 2], 2]')


def test_string_in_list_assignment():
    sim_assert("foo := [['cat']]; foo @ 0 @ 0 @ 2 := 'b'; write foo", '[[cab]]')


def test_string_non_char_assignment():
    sim_assert_error(
        "foo := 'cat'; foo @ 0 := 'ab'",
        'Illegal type conversion from non-character to character'
    )
    sim_assert_error(
        "foo := 'cat'; foo @ 0 := 3",
        'Illegal type conversion from non-character to character'
    )


def test_non_symbolic_assignment():
    sim_assert_error('0 := 1', 'Non-symbolic assignment')


def test_unassigned_symbol():
    sim_assert_error(
        'write foo',
        "Unassigned symbol `foo' used in expression"
    )
    sim_assert_error(
        'x := foo',
        "Unassigned symbol `foo' used in expression"
    )
    sim_assert_error(
        'write [[[foo]]]',
        "Unassigned symbol `foo' used in expression"
    )
    sim_assert_error(
        'x := [[[foo]]]',
        "Unassigned symbol `foo' used in expression"
    )


def test_multiple_assignment():
    sim_assert_error(
        'a := b := 0',
        "Multiple assignment is not supported"
    )


def test_assignment_index_out_of_bounds():
    sim_assert_error('a := [0]; a @ 1 := 0', 'Index 1 is out of bounds')
    sim_assert_error('a := [0]; a @ -2 := 0', 'Index -2 is out of bounds')


def test_complicated_array_assignment():
    sim_assert('''
        a := [0, [1, 2, 8], [5, 7], 3]
        a @ 3 := [2, 3]
        a @ 3 @ 0 := []
        a @ 1 := 4
        write a
    ''', '[0, 4, [5, 7], [[], 3]]')


def test_assign_zoe():
    sim_assert_error('zoe := 0', "Illegal assignment of special symbol `zoe'")
    sim_assert_error('zoe @ 0 := 0', "Illegal assignment of special symbol `zoe'")


def test_set_index_unassigned_symbol():
    sim_assert_error(
        'foo @ 3 = 1',
        "Unassigned symbol `foo' used in expression"
    )
