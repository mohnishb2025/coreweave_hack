from b58 import decode

def test_two_digits():
    assert decode("21") == 58
