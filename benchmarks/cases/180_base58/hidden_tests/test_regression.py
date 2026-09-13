from b58 import decode

def test_other_digits_and_letter():
    assert decode("15") == 4
    assert decode("z") == 57
