from zoe.test import sim_assert, sim_assert_error


def test_unclosed_string_literal():
    sim_assert_error("writeln 'Hello, world", 'Unclosed string literal')
    sim_assert_error("writeln 'Hello, world''", 'Unclosed string literal')


def test_unknown_token():
    sim_assert_error("write ^", "Unknown token `^'")
    sim_assert_error("write :-", "Unknown token `:-'")
    sim_assert_error("write :", "Unknown token `:'")
    sim_assert_error("write 0.0", "Unknown token `.'")


def test_id_token():
    sim_assert("_a_b_c_0 := 10; write _a_b_c_0", "10")
    sim_assert_error("0a_b_c_0 := 10; write 0a_b_c_0", "Invalid expression")
