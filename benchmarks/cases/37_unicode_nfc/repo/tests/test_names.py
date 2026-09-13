from names import lookup

def test_composed_and_decomposed_cafe_match():
    table = {"caf\u00e9": 1}
    assert lookup(table, "cafe\u0301") == 1
