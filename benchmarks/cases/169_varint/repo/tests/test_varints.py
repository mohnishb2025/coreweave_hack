from varints import decode

def test_two_byte_300():
    assert decode(bytes([0xAC, 0x02])) == 300
