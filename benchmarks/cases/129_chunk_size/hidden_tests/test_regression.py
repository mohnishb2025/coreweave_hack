from chunks import size

def test_extension_and_uppercase():
    assert size("1A;ext=1") == 26
    assert size("10") == 16
