from filesafe import safe

def test_reserved_aux():
    assert safe("aux.txt") == "_aux.txt"
