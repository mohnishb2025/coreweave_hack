from bases import parse_int

def test_bin_oct_and_sign():
    assert parse_int("0b1010") == 10
    assert parse_int("0o10") == 8
    assert parse_int("+10") == 10
    assert parse_int("10") == 10
