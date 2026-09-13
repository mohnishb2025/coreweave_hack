from json5s import load

def test_trailing_comma_array():
    assert load("[1, 2,]") == [1, 2]
