from pads import decode

def test_missing_padding():
    assert decode("MFRGG") == b"abc"
