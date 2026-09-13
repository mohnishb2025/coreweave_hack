from colors import expand

def test_bare_short_and_long():
    assert expand("def") == "#ddeeff"
    assert expand("#AABBCC") == "#aabbcc"
