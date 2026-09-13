from tokens import decode

def test_url_safe_alphabet_without_padding():
    assert decode("-_8") == b"\xfb\xff"
