from dnsnames import valid

def test_hyphen_length_and_ok():
    assert valid("-bad") is False
    assert valid("a" * 64) is False
    assert valid("web-1") is True
