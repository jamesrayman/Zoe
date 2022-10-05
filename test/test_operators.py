from zoe.test import sim_assert, sim_assert_error


# Not
def test_not_int():
    sim_assert("write ~0", '1')
    sim_assert("write ~1", '0')
    sim_assert("write ~2", '0')
    sim_assert("write ~-1", '0')


def test_not_string():
    sim_assert("write ~''", '1')
    sim_assert("write ~'0'", '0')
    sim_assert("write ~'hello'", '0')


def test_not_list():
    sim_assert("write ~[]", '1')
    sim_assert("write ~['']", '0')
    sim_assert("write ~[0, 1, 2]", '0')


def test_not_block():
    sim_assert("write ~{}", '1')
    sim_assert("write ~{0}", '0')
    sim_assert("write ~{ writeln 'hello' }", '0')


# Size
def test_size_string():
    sim_assert("write #'hello'", '5')


def test_size_list():
    sim_assert("write #[1, 'hello', -1]", '3')


def test_size_int():
    sim_assert_error('write #0', "Illegal operation `#' with operand of kind Integer")


def test_size_block():
    sim_assert_error("write #{}", "Illegal operation `#' with operand of kind Block")


# Unary Plus
def test_unary_plus_string():
    sim_assert("write 2 ++ '2'", '4')
    sim_assert("write 2 ++ ' -1 \n'", '1')


def test_unary_plus_non_numeric_string():
    sim_assert_error(
        "write +'hello'",
        'Illegal type conversion from non-numeric String to Integer'
    )


def test_unary_plus_int():
    sim_assert("write 2 ++ 2", '4')


def test_unary_plus_block():
    sim_assert_error("write +{}", 'Illegal type conversion from Block to Integer')


def test_unary_plus_list():
    sim_assert_error("write +[]", 'Illegal type conversion from List to Integer')


# Unary Minus
def test_unary_minus_string_int():
    sim_assert("write -'2' + 1", '-1')


# At
def test_at_list_int():
    sim_assert("write [3, 4, 5] @ 1", '4')
    sim_assert("write [3, 4, 5] @ -1", '5')


def test_at_list_int_out_of_bounds():
    sim_assert_error("write [3, 4, 5] @ 3", 'Index 3 is out of bounds')
    sim_assert_error("write [] @ 0", 'Index 0 is out of bounds')
    sim_assert_error("write [3, 4, 5] @ -4", 'Index -4 is out of bounds')


def test_at_string_int():
    sim_assert("write 'bar' @ 1", 'a')
    sim_assert("write 'bar' @ -1", 'r')


def test_at_string_int_out_of_bounds():
    sim_assert_error("write 'foo' @ 3", 'Index 3 is out of bounds')
    sim_assert_error("write '' @ 0", 'Index 0 is out of bounds')
    sim_assert_error("write 'foo' @ -4", 'Index -4 is out of bounds')


def test_at_block_int():
    sim_assert_error(
        'write { write 0 } @ 0',
        "Illegal operation `@' with operands of kind Block and Integer"
    )


def test_at_int_int():
    sim_assert_error(
        'write 0 @ 0',
        "Illegal operation `@' with operands of kind Integer and Integer"
    )


def test_at_list_list():
    sim_assert_error(
        'write [10] @ [10]',
        "Illegal operation `@' with operands of kind List and List"
    )


# Pow
def test_pow_int_int():
    sim_assert('write 2 ** 10', '1024')
    sim_assert('write 7 ** 0', '1')
    sim_assert('write 0 ** 0', '1')


def test_pow_negative_int_int():
    sim_assert('write (-3) ** 3', '-27')
    sim_assert('write (-3) ** 4', '81')
    sim_assert('write (-1) ** (-2)', '1')
    sim_assert('write (-1) ** (-3)', '-1')
    sim_assert_error('write 0 ** (-2)', 'Division by 0')
    sim_assert_error('write 2 ** (-2)', 'Fractional values are not supported')


def test_pow_int_string():
    sim_assert_error(
        "write 4 ** '2'",
        "Illegal operation `**' with operands of kind Integer and String"
    )


# Times
def test_times_int_int():
    sim_assert('write 4 * 7', '28')


def test_times_int_string():
    sim_assert("write 3 * 'hello '", 'hello hello hello ')
    sim_assert("write 'hello ' * 3", 'hello hello hello ')
    sim_assert("write 0 * 'hello '", '')
    sim_assert("write (-3) * 'hello '", '')


def test_times_int_list():
    sim_assert("write 3 * [0, 1, 2]", '[0, 1, 2, 0, 1, 2, 0, 1, 2]')
    sim_assert("write [0, 1, 2] * 3", '[0, 1, 2, 0, 1, 2, 0, 1, 2]')
    sim_assert("write 0 * [0, 2]", '[]')
    sim_assert("write (-3) * [0, 2]", '[]')


def test_times_int_block():
    sim_assert("i := 0; 4 * { write i; i := i + 1 }; write i", '01234')
    sim_assert("i := 0; { write i; i := i + 1 } * 4; write i", '01234')
    sim_assert("i := 0; 0 * { write i; i := i + 1 }; write i", '0')
    sim_assert("i := 0; (-1) * { write i; i := i + 1 }; write i", '0')


def test_times_string_list():
    sim_assert_error(
        "write 'hello' * [0, 1, 2]",
        "Illegal operation `*' with operands of kind String and List"
    )


# Divide
def test_divide_int_int():
    sim_assert('write 12 / 4', '3')
    sim_assert('write 100 / 6', '16')
    sim_assert('write 100 / -6', '-17')
    sim_assert('write -100 / -6', '16')
    sim_assert('write -100 / 6', '-17')


def test_divide_division_by_zero():
    sim_assert_error('1 / 0', 'Division by 0')


def test_divide_int_string():
    sim_assert_error(
        "write 4 / '2'",
        "Illegal operation `/' with operands of kind Integer and String"
    )


# Mod
def test_mod_int_int():
    sim_assert('write 12 % 4', '0')
    sim_assert('write 100 % 6', '4')
    sim_assert('write 100 % -6', '-2')
    sim_assert('write -100 % -6', '-4')
    sim_assert('write -100 % 6', '2')


def test_mod_division_by_zero():
    sim_assert_error('1 % 0', 'Division by 0')


def test_mod_int_string():
    sim_assert_error(
        "write 4 % '2'",
        "Illegal operation `%' with operands of kind Integer and String"
    )


# Plus
def test_plus_int_int():
    sim_assert('write 2 + 2', '4')


def test_plus_string_string():
    sim_assert("write '2' + '3'", '23')


def test_plus_string_int():
    sim_assert("write 2 + '3'", '23')
    sim_assert("write (-2) + '3'", '-23')


def test_plus_int_string():
    sim_assert("write '2' + 3", '23')
    sim_assert("write '2' + -3", '2-3')


def test_plus_list_list():
    sim_assert("write [1, 2] + [0, 3]", '[1, 2, 0, 3]')


def test_plus_string_list():
    sim_assert("write 'hello ' + [0, 3]", 'hello [0, 3]')


def test_plus_int_list():
    sim_assert_error(
        "write 0 + [0, 3]",
        "Illegal operation `+' with operands of kind Integer and List"
    )


def test_plus_block_block():
    sim_assert(
        "foo := { write 'hello ' } + { write 'world ' }; foo + foo",
        'hello world hello world '
    )


def test_plus_int_block():
    sim_assert_error(
        "write 0 + { write 1 }",
        "Illegal operation `+' with operands of kind Integer and Block"
    )


# Minus
def test_minus_int_int():
    sim_assert('write 4 - 2', '2')


def test_minus_int_string():
    sim_assert_error(
        "write 4 - '2'",
        "Illegal operation `-' with operands of kind Integer and String"
    )


# And
def test_and_truthy():
    sim_assert(r"write '0' /\ 5", '5')
    sim_assert(r"write 1 /\ 5", '5')


def test_and_falsy():
    sim_assert(r"write [] /\ 5", '[]')
    sim_assert(r"write 0 /\ 5", '0')


# Or
def test_or_truthy():
    sim_assert(r"write '0' \/ 5", '0')
    sim_assert(r"write 1 \/ 5", '1')


def test_or_falsy():
    sim_assert(r"write [] \/ 5", '5')
    sim_assert(r"write 0 \/ 5", '5')


# Eq
def test_eq_int_int():
    sim_assert('write 1 = 1', '1')
    sim_assert('write 2 = 1', '0')
    sim_assert('write 1 = 2', '0')


def test_eq_int_string():
    sim_assert("write 1 = '1'", '0')


def test_eq_block_string():
    sim_assert("write { '1' } = '1'", '0')


def test_eq_block_block():
    sim_assert("write { write a } = { write a }", '1')
    sim_assert("write { write b } = { write a }", '0')


def test_eq_list_list():
    sim_assert("write [1, [1, 2, []], 3] = [1, [1, 2, []]] + [3]", '1')
    sim_assert("write [1, [1, 2, []], 3] = [1, [0, 2, []]] + [3]", '0')


def test_eq_string_string():
    sim_assert("write 'hell' + 'o' = 'hello'", '1')
    sim_assert("write 'Hell' + 'o' = 'hello'", '0')


# Neq
def test_neq_int_int():
    sim_assert('write 1 /= 1', '0')
    sim_assert('write 2 /= 1', '1')
    sim_assert('write 1 /= 2', '1')


def test_neq_int_string():
    sim_assert("write 1 /= '1'", '1')


def test_neq_block_block():
    sim_assert("write { write b } /= { write a }", '1')


# Less
def test_less_int_int():
    sim_assert('write 1 < 1', '0')
    sim_assert('write 2 < 1', '0')
    sim_assert('write 1 < 2', '1')


def test_less_int_string():
    sim_assert_error(
        "write 1 < '1'",
        "Illegal operation `<' with operands of kind Integer and String"
    )


def test_less_block_block():
    sim_assert_error(
        "write {} < {}",
        "Illegal operation `<' with operands of kind Block and Block"
    )


def test_less_string_string():
    sim_assert("write 'Hello, world' < 'Hello, world'", '0')
    sim_assert("write 'Hello,' < 'Hello, world'", '1')
    sim_assert("write 'Hello, w aardvark' < 'Hello, v zebra'", '0')


def test_less_list_list():
    sim_assert("write [] < []", '0')
    sim_assert("write [1, 2, 3] < [3, 2, 1]", '1')
    sim_assert("write [1, 'hell', 1] < [1, 'hello', 1]", '1')
    sim_assert("write [1, [0, 'a', 3], 1] < [1, [0, 'a', 0], 1]", '0')
    sim_assert_error(
        "write [0, 1, [3, 3]] < [0, 1, [3, '3']]",
        "Illegal operation `<' with operands of kind Integer and String"
    )


# Greater
def test_greater_int_int():
    sim_assert('write 1 > 1', '0')
    sim_assert('write 2 > 1', '1')
    sim_assert('write 1 > 2', '0')


def test_greater_int_string():
    sim_assert_error(
        "write 1 > '1'",
        "Illegal operation `>' with operands of kind Integer and String"
    )


def test_greater_block_block():
    sim_assert_error(
        "write {} > {}",
        "Illegal operation `>' with operands of kind Block and Block"
    )


# Leq
def test_leq_int_int():
    sim_assert('write 1 <= 1', '1')
    sim_assert('write 2 <= 1', '0')
    sim_assert('write 1 <= 2', '1')


def test_leq_int_string():
    sim_assert_error(
        "write 1 <= '1'",
        "Illegal operation `<=' with operands of kind Integer and String"
    )


def test_leq_block_block():
    sim_assert_error(
        "write {} <= {}",
        "Illegal operation `<=' with operands of kind Block and Block"
    )


# Geq
def test_geq_int_int():
    sim_assert('write 1 >= 1', '1')
    sim_assert('write 2 >= 1', '1')
    sim_assert('write 1 >= 2', '0')


def test_geq_int_string():
    sim_assert_error(
        "write 1 >= '1'",
        "Illegal operation `>=' with operands of kind Integer and String"
    )


def test_geq_block_block():
    sim_assert_error(
        "write {} >= {}",
        "Illegal operation `>=' with operands of kind Block and Block"
    )
