from varints import decode

def test_single_byte_and_400():
    assert decode(bytes([0x01])) == 1
    assert decode(bytes([0x90, 0x03])) == 400
