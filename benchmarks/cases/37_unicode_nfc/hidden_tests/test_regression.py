from names import lookup

def test_both_sides_normalize():
    table = {"a\u0308": 7, "n\u0303": 8}
    assert lookup(table, "\u00e4") == 7
    assert lookup({"\u00f1": 3}, "n\u0303") == 3
