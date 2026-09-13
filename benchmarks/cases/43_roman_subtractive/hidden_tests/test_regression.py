from roman import to_int

def test_later_subtractive_and_compound_values():
    assert to_int("IX") == 9
    assert to_int("XL") == 40
    assert to_int("CM") == 900
    assert to_int("MCMXC") == 1990
    assert to_int("III") == 3
