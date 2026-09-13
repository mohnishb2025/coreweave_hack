from pads import decode

def test_lowercase_and_longer():
    assert decode("mfrgg") == b"abc"
    assert decode("MFRGGZA") == b"abcd"
