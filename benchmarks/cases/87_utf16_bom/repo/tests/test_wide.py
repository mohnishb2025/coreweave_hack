from wide import decode

def test_le_bom_is_not_in_the_text():
    assert decode(b"\xff\xfeh\x00i\x00") == "hi"
