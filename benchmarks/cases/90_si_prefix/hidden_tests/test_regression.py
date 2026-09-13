from units import to_number

def test_mega_and_plain():
    assert to_number("2M") == 2_000_000
    assert to_number("250") == 250
