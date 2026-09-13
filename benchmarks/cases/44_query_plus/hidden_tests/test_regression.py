from query import decode

def test_percent_space_and_literal_plus():
    assert decode("a%20b") == "a b"
    assert decode("a%2Bb") == "a+b"
    assert decode("a+b%20c") == "a b c"
