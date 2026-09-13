from wide import decode

def test_be_bom_and_le_without_bom():
    assert decode(b"\xfe\xff\x00h\x00i") == "hi"
    assert decode(b"h\x00i\x00") == "hi"
