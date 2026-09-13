from units import to_number

def test_kilo_suffix():
    assert to_number("1.5k") == 1500
