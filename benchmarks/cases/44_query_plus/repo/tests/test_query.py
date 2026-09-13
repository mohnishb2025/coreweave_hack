from query import decode

def test_plus_is_a_space_in_form_encoding():
    assert decode("a+b") == "a b"
