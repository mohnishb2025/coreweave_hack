from bases import parse_int

def test_hex_prefix_is_base_16():
    assert parse_int("0x10") == 16
