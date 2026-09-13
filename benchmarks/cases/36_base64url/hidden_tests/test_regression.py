from tokens import decode

def test_standard_and_unpadded_payloads():
    assert decode("aGk") == b"hi"
    assert decode("+/8=") == b"\xfb\xff"
    assert decode("YQ") == b"a"
